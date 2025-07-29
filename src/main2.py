from data.GapInstance import create_local_search_favored_instance
from solvers.greedy_solver import greedy_assignment, calculate_total_cost
from solvers.local_search_solver import local_search_assignment
from solvers.naive_solver import naive_assignment
from visualisation.plot_assignment import plot_assignment

import time
import copy


def calculate_assignment_quality(instance, assignment, label=""):
    total_cost = calculate_total_cost(instance, assignment)
    assigned_count = sum(1 for a in assignment.values() if a != -1)
    print(f"\n{label} - Evaluacija:")
    print(f"Ukupan trošak: {total_cost}")
    print(f"Dodeljeni zadaci: {assigned_count}/{len(assignment)}")


if __name__ == "__main__":
    original_instance = create_local_search_favored_instance()

    instance_greedy = copy.deepcopy(original_instance)
    print("\n--- Greedy Assignment ---")
    start_greedy = time.time()
    greedy = greedy_assignment(instance_greedy)
    end_greedy = time.time()
    for task_id, agent_id in greedy.items():
        print(f"Task {task_id} → Agent {agent_id}" if agent_id != -1 else f"Task {task_id} → Nije moguće dodeliti")
    calculate_assignment_quality(instance_greedy, greedy, "Greedy")
    print(f"Vreme izvršavanja: {end_greedy - start_greedy:.4f} sekundi")
    plot_assignment(instance_greedy, greedy)

    instance_local = copy.deepcopy(original_instance)
    print("\n--- Local Search Assignment ---")
    start_local = time.time()
    local = local_search_assignment(instance_local)
    end_local = time.time()
    for task_id, agent_id in local.items():
        print(f"Task {task_id} → Agent {agent_id}" if agent_id != -1 else f"Task {task_id} → Nije moguće dodeliti")
    calculate_assignment_quality(instance_local, local, "Local Search")
    print(f"Vreme izvršavanja: {end_local - start_local:.4f} sekundi")
    plot_assignment(instance_local, local)

    instance_naive = copy.deepcopy(original_instance)
    print("\n--- Naive Assignment ---")
    start_naive = time.time()
    naive = naive_assignment(instance_naive)
    end_naive = time.time()
    for task_id, agent_id in naive.items():
        print(f"Task {task_id} → Agent {agent_id}" if agent_id != -1 else f"Task {task_id} → Nije moguće dodeliti")
    calculate_assignment_quality(instance_naive, naive, "Naive")
    print(f"Vreme izvršavanja: {end_naive - start_naive:.4f} sekundi")
    plot_assignment(instance_naive, naive)
