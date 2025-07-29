from data.GapInstance import create_test_instance, create_large_test_instance
from solvers.greedy_solver import calculate_total_cost, greedy_assignment
from visualisation.plot_assignment import plot_assignment


if __name__ == "__main__":
    instance = create_large_test_instance()
    print(instance)

    print("\n--- Greedy Assignment ---")
    assignment = greedy_assignment(instance)

    for task_id, agent_id in assignment.items():
        if agent_id != -1:
            print(f"Task {task_id} → Agent {agent_id}")
        else:
            print(f"Task {task_id} → Nije moguće dodeliti nijednom agentu")

    total_cost = calculate_total_cost(instance, assignment)
    print(f"\nUkupan trošak: {total_cost}")
    plot_assignment(instance, assignment)


