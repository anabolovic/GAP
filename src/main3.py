import time
import copy

from Battlefild import *
from solvers.simulated_annealing import simulated_annealing, simulated_annealing_v2
from solvers.greedy_solver import greedy_assignment, calculate_total_cost
from solvers.naive_solver import naive_assignment
from visualisation.plot_assignment import plot_assignment

import random
from data.GapInstance import GAPInstance
from models.Agent import Agent
from models.Task import Task


def generate_hard_instance(num_agents=30, num_tasks=300, seed=42):
    random.seed(seed)

    agents = []
    for i in range(num_agents):
        capacity = random.randint(100, 200)
        agents.append(Agent(i, capacity))

    tasks = []
    for t in range(num_tasks):
        costs = []
        demands = []

        for a in range(num_agents):

            if a < 3:
                costs.append(random.randint(1, 5))
                demands.append(random.randint(30, 50))
            else:
                costs.append(random.randint(40, 100))
                demands.append(random.randint(5, 20))


        tasks.append(Task(t, demands, costs))

    return GAPInstance(agents, tasks)



def calculate_assignment_quality(instance, assignment, label=""):
    total_cost = calculate_total_cost(instance, assignment)
    assigned_count = sum(1 for a in assignment.values() if a != -1)
    print(f"\n{label} - Evaluacija:")
    print(f"Ukupan trošak: {total_cost}")
    print(f"Dodeljeni zadaci: {assigned_count}/{len(assignment)}")


if __name__ == "__main__":
    original_instance = generate_hard_instance()

    instance_sa = copy.deepcopy(original_instance)
    print("\n--- Simulated Annealing Assignment (v1) ---")
    start_sa = time.time()
    sa_assignment = simulated_annealing(instance_sa)
    end_sa = time.time()
    for task_id, agent_id in sa_assignment.items():
        print(f"Task {task_id} → Agent {agent_id}" if agent_id != -1 else f"Task {task_id} → Nije moguće dodeliti")
    calculate_assignment_quality(instance_sa, sa_assignment, "Simulated Annealing v1")
    print(f"Vreme izvršavanja: {end_sa - start_sa:.4f} sekundi")
    plot_assignment(instance_sa, sa_assignment, "Simulated Annealing v1")

    instance_sa2 = copy.deepcopy(original_instance)
    print("\n--- Simulated Annealing Assignment (v2) ---")
    start_sa2 = time.time()
    sa2_assignment = simulated_annealing_v2(
        instance_sa2,
        initial_temp=1200.0,
        min_temp=1e-3,
        max_iter=15000,
        cooling="geometric",     # "geometric" | "linear" | "log"
        alpha=0.996,
        acceptance="cauchy",     # "boltzmann" | "cauchy" | "sigmoid"
        neighborhood="mixed",    # "swap" | "move" | "mixed"
        moves_per_step=(1, 4),
        seed=42
    )
    end_sa2 = time.time()
    # for task_id, agent_id in sa2_assignment.items():
    #    print(f"Task {task_id} → Agent {agent_id}" if agent_id != -1 else f"Task {task_id} → Nije moguće dodeliti")
    calculate_assignment_quality(instance_sa2, sa2_assignment, "Simulated Annealing v2")
    print(f"Vreme izvršavanja: {end_sa2 - start_sa2:.4f} sekundi")
    plot_assignment(instance_sa2, sa2_assignment, "Simulated Annealing v2")

    instance_greedy = copy.deepcopy(original_instance)
    print("\n--- Greedy Assignment ---")
    start_greedy = time.time()
    greedy = greedy_assignment(instance_greedy)
    end_greedy = time.time()
    #for task_id, agent_id in greedy.items():
    #    print(f"Task {task_id} → Agent {agent_id}" if agent_id != -1 else f"Task {task_id} → Nije moguće dodeliti")
    calculate_assignment_quality(instance_greedy, greedy, "Greedy")
    print(f"Vreme izvršavanja: {end_greedy - start_greedy:.4f} sekundi")
    plot_assignment(instance_greedy, greedy, "Greedy")

    instance_random = copy.deepcopy(original_instance)
    print("\n--- Random Assignment ---")
    start_random = time.time()
    rnd = random_assignment(instance_random)
    end_random = time.time()
    #for task_id, agent_id in rnd.items():
    #    print(f"Task {task_id} → Agent {agent_id}" if agent_id != -1 else f"Task {task_id} → Nije moguće dodeliti")
    calculate_assignment_quality(instance_random, rnd, "Random")
    print(f"Vreme izvršavanja: {end_random - start_random:.4f} sekundi")
    plot_assignment(instance_random, rnd, "Random")

    instance_naive = copy.deepcopy(original_instance)
    print("\n--- Naive Assignment ---")
    start_naive = time.time()
    naive = naive_assignment(instance_naive)
    end_naive = time.time()
    #for task_id, agent_id in naive.items():
    #    print(f"Task {task_id} → Agent {agent_id}" if agent_id != -1 else f"Task {task_id} → Nije moguće dodeliti")
    calculate_assignment_quality(instance_naive, naive, "Naive")
    print(f"Vreme izvršavanja: {end_naive - start_naive:.4f} sekundi")
    plot_assignment(instance_naive, naive, "Naive")

    print("\n--- SA v2 mini-experiments ---")
    sa_variants = [
        {"cooling": "geometric", "alpha": 0.996, "acceptance": "boltzmann", "neighborhood": "mixed"},
        {"cooling": "geometric", "alpha": 0.994, "acceptance": "cauchy",    "neighborhood": "mixed"},
        {"cooling": "log",       "alpha": 0.0,   "acceptance": "sigmoid",   "neighborhood": "move"},
        {"cooling": "linear",    "alpha": 0.0,   "acceptance": "boltzmann", "neighborhood": "swap"},
    ]
    for i, cfg in enumerate(sa_variants, 1):
        inst = copy.deepcopy(original_instance)
        label = f"SA v2 #{i} ({cfg['cooling']}, {cfg['acceptance']}, {cfg['neighborhood']})"
        t0 = time.time()
        sol = simulated_annealing_v2(
            inst,
            initial_temp=1200.0,
            min_temp=1e-3,
            max_iter=12000,
            cooling=cfg["cooling"],
            alpha=cfg["alpha"],
            acceptance=cfg["acceptance"],
            neighborhood=cfg["neighborhood"],
            moves_per_step=(1, 4),
            seed=42 + i
        )
        t1 = time.time()
        calculate_assignment_quality(inst, sol, label)
        print(f"{label} – vreme: {t1 - t0:.4f} s")
        plot_assignment(inst, sol, label)
