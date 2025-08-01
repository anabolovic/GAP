import random
import math
import copy

from solvers.greedy_solver import greedy_assignment

def simulated_annealing(instance, initial_temp=1000, cooling_rate=0.995, min_temp=1e-3, max_iter=10000):
    current_solution = greedy_assignment(instance)
    current_cost = calculate_total_cost(instance, current_solution)

    best_solution = copy.deepcopy(current_solution)
    best_cost = current_cost

    temp = initial_temp
    iteration = 0

    while temp > min_temp and iteration < max_iter:
        new_solution = neighbor_solution(instance, current_solution)
        new_cost = calculate_total_cost(instance, new_solution)

        delta = new_cost - current_cost

        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temp):
            current_solution = new_solution
            current_cost = new_cost

            if current_cost < best_cost:
                best_solution = copy.deepcopy(current_solution)
                best_cost = current_cost

        temp *= cooling_rate
        iteration += 1

    return best_solution


def neighbor_solution(instance, solution):
    new_solution = copy.deepcopy(solution)
    num_tasks = len(instance.tasks)
    num_agents = len(instance.agents)

    # Probaj do 5 promena po iteraciji
    for _ in range(random.randint(1, 5)):
        task_id = random.randint(0, num_tasks - 1)
        current_agent = new_solution[task_id]

        # Probaj da zameniš i sa drugim taskom (SWAP)
        swap_task_id = random.randint(0, num_tasks - 1)
        if swap_task_id != task_id:
            agent1 = new_solution[task_id]
            agent2 = new_solution[swap_task_id]

            # Probaj zamenu ako je validna
            task1 = instance.tasks[task_id]
            task2 = instance.tasks[swap_task_id]
            if (instance.agents[agent2].can_assign(task1, agent2) and
                instance.agents[agent1].can_assign(task2, agent1)):
                new_solution[task_id] = agent2
                new_solution[swap_task_id] = agent1
                continue

        # Inače pokušaj zamenu jednog agenta
        candidate_agents = [
            agent_id for agent_id in range(num_agents)
            if agent_id != current_agent and instance.agents[agent_id].can_assign(instance.tasks[task_id], agent_id)
        ]
        if candidate_agents:
            new_solution[task_id] = random.choice(candidate_agents)

    return new_solution



def calculate_total_cost(instance, solution):
    total = 0
    for task_id, agent_id in solution.items():
        if isinstance(agent_id, int) and 0 <= agent_id < len(instance.agents):
            total += instance.tasks[task_id].costs[agent_id]
        else:
            print(f"[WARNING] Nevalidan agent_id={agent_id} za task_id={task_id}")
            total += 1e9
    return total

