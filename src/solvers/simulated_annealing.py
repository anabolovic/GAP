import random
import math
import copy

from solvers.greedy_solver import greedy_assignment


def calculate_total_cost(instance, solution):
    total = 0
    for task_id, agent_id in solution.items():
        if isinstance(agent_id, int) and 0 <= agent_id < len(instance.agents):
            total += instance.tasks[task_id].costs[agent_id]
        else:
            # Fail-safe: penalizuj nevalidno stanje
            total += 1e9
    return total

# Strategije susedstva
def _neighbor_swap(instance, solution):
    """Zameni agente na dva različita taska ako je validno (SWAP)."""
    new_solution = copy.deepcopy(solution)
    num_tasks = len(instance.tasks)

    # probaj do 5 puta da nađeš validan swap
    for _ in range(5):
        t1 = random.randrange(num_tasks)
        t2 = random.randrange(num_tasks)
        if t1 == t2:
            continue

        a1 = new_solution[t1]
        a2 = new_solution[t2]
        if a1 == a2:
            continue

        task1 = instance.tasks[t1]
        task2 = instance.tasks[t2]

        # Proveri da li bi zamena bila validna po kapacitetima:
        if (instance.agents[a2].can_assign(task1, a2) and
            instance.agents[a1].can_assign(task2, a1)):
            new_solution[t1], new_solution[t2] = a2, a1
            return new_solution

    return new_solution  # ako ništa validno, vrati isto


def _neighbor_move(instance, solution):
    """Premesti jedan task na drugog agenta ako je validno (MOVE)."""
    new_solution = copy.deepcopy(solution)
    num_tasks = len(instance.tasks)
    num_agents = len(instance.agents)

    t = random.randrange(num_tasks)
    current_agent = new_solution[t]

    # kandidati: svi drugi agenti koji mogu da preuzmu task t
    candidates = [
        a for a in range(num_agents)
        if a != current_agent and instance.agents[a].can_assign(instance.tasks[t], a)
    ]
    if candidates:
        new_solution[t] = random.choice(candidates)

    return new_solution


def _neighbor_mixed(instance, solution):
    """Kombinuje swap i move."""
    if random.random() < 0.5:
        return _neighbor_swap(instance, solution)
    return _neighbor_move(instance, solution)


_NEIGHBOR_BY_NAME = {
    "swap": _neighbor_swap,
    "move": _neighbor_move,
    "mixed": _neighbor_mixed,
}



# Prihvatne funkcije
def _accept_prob(delta, temp, mode="boltzmann"):
    """
    delta = new_cost - current_cost (pozitivno je lošije)
    """
    if delta <= 0:
        return 1.0

    if temp <= 0:
        return 0.0

    if mode == "boltzmann":
        # klasično SA: exp(-Δ/T)
        return math.exp(-delta / temp)
    elif mode == "cauchy":
        # Cauchy (hladnije daje sporiji pad): 1 / (1 + Δ/T)
        return 1.0 / (1.0 + (delta / temp))
    elif mode == "sigmoid":
        # Sigmoid: 1 / (1 + exp(Δ/T)) -> mekši cutoff od Boltzmanna
        return 1.0 / (1.0 + math.exp(delta / temp))
    else:
        # default na boltzmann
        return math.exp(-delta / temp)



# Sheme hlađenja
def _next_temp(temp, step, initial_temp, max_iter, mode="geometric", alpha=0.995):
    if mode == "geometric":
        # T_{k+1} = alpha * T_k
        return temp * alpha
    elif mode == "linear":
        # linearni pad od T0 do ~0: T_k = T0 * (1 - k/max_iter)
        frac = max(0.0, 1.0 - (step / max_iter))
        return initial_temp * max(frac, 1e-12)
    elif mode == "log":
        # logaritamski: T_k = T0 / log(k + c); c=2 da izbegnemo log(1)
        return initial_temp / max(math.log(step + 2.0), 1.0)
    # default
    return temp * alpha


def simulated_annealing(
    instance,
    initial_temp=1000.0,
    min_temp=1e-3,
    max_iter=10000,
    cooling="geometric",
    alpha=0.995,
    acceptance="boltzmann",
    neighborhood="mixed",
    moves_per_step=(1, 5),
    seed=None
):
    """Zadržavamo staro ime radi kompatibilnosti sa Battlefild.py i drugim importima."""
    return simulated_annealing_v2(
        instance=instance,
        initial_temp=initial_temp,
        min_temp=min_temp,
        max_iter=max_iter,
        cooling=cooling,
        alpha=alpha,
        acceptance=acceptance,
        neighborhood=neighborhood,
        moves_per_step=moves_per_step,
        seed=seed,
    )


# Nova varijanta SA
def simulated_annealing_v2(
    instance,
    initial_temp=1000.0,
    min_temp=1e-3,
    max_iter=10000,
    cooling="geometric",      # "geometric" | "linear" | "log"
    alpha=0.995,              # parametar za cooling (npr. geometric alpha)
    acceptance="boltzmann",   # "boltzmann" | "cauchy" | "sigmoid"
    neighborhood="mixed",     # "swap" | "move" | "mixed"
    moves_per_step=(1, 5),    # (min,max) - koliko izmjena po iteraciji
    seed=None
):
    """
    Drop-in zamena koja dodaje:
      - više cooling schedule varijanti,
      - više acceptance varijanti,
      - više strategija susedstva.

    Vraća best_solution (kao i tvoja originalna funkcija).
    """
    if seed is not None:
        random.seed(seed)

    # inicijalno rešenje iz greedy-ja (isti pristup kao kod tebe)
    current_solution = greedy_assignment(instance)
    current_cost = calculate_total_cost(instance, current_solution)

    best_solution = copy.deepcopy(current_solution)
    best_cost = current_cost

    temp = float(initial_temp)

    # odaberi funkciju susedstva
    neighbor_fn = _NEIGHBOR_BY_NAME.get(neighborhood, _neighbor_mixed)

    for step in range(1, max_iter + 1):
        # koliko lokalnih poteza odradimo u ovoj iteraciji
        n_moves = random.randint(moves_per_step[0], moves_per_step[1])

        candidate_solution = copy.deepcopy(current_solution)
        candidate_cost = current_cost

        for _ in range(n_moves):
            neighbor = neighbor_fn(instance, candidate_solution)
            neighbor_cost = calculate_total_cost(instance, neighbor)

            delta = neighbor_cost - candidate_cost
            p = _accept_prob(delta, temp, mode=acceptance)

            if delta <= 0 or random.random() < p:
                candidate_solution = neighbor
                candidate_cost = neighbor_cost

        # Ako je kandidat bolji od trenutnog, pomeri se
        if candidate_cost <= current_cost:
            current_solution = candidate_solution
            current_cost = candidate_cost
        else:
            # dozvoli i skok na lošije sa malom šansom
            delta = candidate_cost - current_cost
            if random.random() < _accept_prob(delta, temp, mode=acceptance):
                current_solution = candidate_solution
                current_cost = candidate_cost

        # update best
        if current_cost < best_cost:
            best_cost = current_cost
            best_solution = copy.deepcopy(current_solution)

        # hlađenje
        temp = _next_temp(temp, step, initial_temp, max_iter, mode=cooling, alpha=alpha)
        if temp < min_temp:
            break

    return best_solution
