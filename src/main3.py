from Battlefild import random_assignment
from solvers.simulated_annealing import simulated_annealing
from solvers.greedy_solver import greedy_assignment, calculate_total_cost
from solvers.naive_solver import naive_assignment
from visualisation.plot_assignment import plot_assignment
from data.BigDataGenerator import generate_hard_instance

import time
import copy


def calculate_assignment_quality(instance, assignment, label=""):
    total_cost = calculate_total_cost(instance, assignment)
    assigned_count = sum(1 for a in assignment.values() if a != -1)
    print(f"\n{label} - Evaluacija:")
    print(f"Ukupan trošak: {total_cost}")
    print(f"Dodeljeni zadaci: {assigned_count}/{len(assignment)}")


if __name__ == "__main__":
    original_instance = generate_hard_instance()

    instance_sa = copy.deepcopy(original_instance)
    print("\n--- Simulated Annealing Assignment ---")
    start_sa = time.time()
    sa_assignment = simulated_annealing(instance_sa)
    end_sa = time.time()
    for task_id, agent_id in sa_assignment.items():
        print(f"Task {task_id} → Agent {agent_id}" if agent_id != -1 else f"Task {task_id} → Nije moguće dodeliti")
    calculate_assignment_quality(instance_sa, sa_assignment, "Simulated Annealing")
    print(f"Vreme izvršavanja: {end_sa - start_sa:.4f} sekundi")
    plot_assignment(instance_sa, sa_assignment, "Simulated Annealing") 

    instance_greedy = copy.deepcopy(original_instance)
    print("\n--- Greedy Assignment ---")
    start_greedy = time.time()
    greedy = greedy_assignment(instance_greedy)
    end_greedy = time.time()
    for task_id, agent_id in greedy.items():
        print(f"Task {task_id} → Agent {agent_id}" if agent_id != -1 else f"Task {task_id} → Nije moguće dodeliti")
    calculate_assignment_quality(instance_greedy, greedy, "Greedy")
    print(f"Vreme izvršavanja: {end_greedy - start_greedy:.4f} sekundi")
    plot_assignment(instance_greedy, greedy, "Greedy")

    instance_random = copy.deepcopy(original_instance)
    print("\n--- Random Assignment ---")
    start_greedy = time.time()
    random = random_assignment(instance_greedy)
    end_random = time.time()
    for task_id, agent_id in random.items():
        print(f"Task {task_id} → Agent {agent_id}" if agent_id != -1 else f"Task {task_id} → Nije moguće dodeliti")
    calculate_assignment_quality(instance_random, random, "Random")
    print(f"Vreme izvršavanja: {end_random - start_greedy:.4f} sekundi")
    plot_assignment(instance_random, random, "Random")

    instance_naive = copy.deepcopy(original_instance)
    print("\n--- Naive Assignment ---")
    start_naive = time.time()
    naive = naive_assignment(instance_naive)
    end_naive = time.time()
    for task_id, agent_id in naive.items():
        print(f"Task {task_id} → Agent {agent_id}" if agent_id != -1 else f"Task {task_id} → Nije moguće dodeliti")
    calculate_assignment_quality(instance_naive, naive, "Naive")
    print(f"Vreme izvršavanja: {end_naive - start_naive:.4f} sekundi")
    plot_assignment(instance_naive, naive, "Naive")