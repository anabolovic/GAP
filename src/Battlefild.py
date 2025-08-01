import copy
from data.BigDataGenerator import generate_hard_instance
from solvers.simulated_annealing import simulated_annealing
from solvers.greedy_solver import greedy_assignment
import random

def calculate_assignment_quality(instance, assignment, label=""):
    total_cost = 0
    agent_loads = {agent.id: 0 for agent in instance.agents}
    valid = True

    for task_id, agent_id in assignment.items():
        if agent_id == -1:
            continue  
        task = instance.tasks[task_id]
        cost = instance.costs[agent_id][task_id]
        load = instance.loads[agent_id][task_id]
        agent_loads[agent_id] += load
        total_cost += cost

    for agent in instance.agents:
        if agent_loads[agent.id] > agent.capacity:
            print(f"[{label}] Agent {agent.id} prekoračio kapacitet: {agent_loads[agent.id]} > {agent.capacity}")
            valid = False

    print(f"[{label}] Ukupan trošak: {total_cost}")
    if valid:
        print(f"[{label}] Rešenje je validno.")
    else:
        print(f"[{label}] Rešenje NIJE validno.")

    return total_cost, valid



def random_assignment(instance):
    solution = {}
    num_agents = len(instance.agents)
    for agent in instance.agents:
        agent.reset() 

    for task_id, task in enumerate(instance.tasks):
        assigned = False
        tried_agents = set()

        while not assigned and len(tried_agents) < num_agents:
            agent_id = random.randint(0, num_agents - 1)
            if agent_id in tried_agents:
                continue
            tried_agents.add(agent_id)

            if instance.agents[agent_id].can_assign(task, agent_id):
                instance.agents[agent_id].remaining_capacity -= task.demands[agent_id]
                solution[task_id] = agent_id
                assigned = True

        if not assigned:
            solution[task_id] = -1

    return solution


if __name__ == "__main__":
    instance_hard = generate_hard_instance()

    print("\n--- Greedy Assignment ---")
    solution_greedy = greedy_assignment(copy.deepcopy(instance_hard))
    calculate_assignment_quality(instance_hard, solution_greedy)

    print("\n--- Simulated Annealing Assignment ---")
    solution_sa = simulated_annealing(copy.deepcopy(instance_hard))
    calculate_assignment_quality(instance_hard, solution_sa)

    print("\n--- Random Assignment ---")
    solution_rand = random_assignment(copy.deepcopy(instance_hard))
    calculate_assignment_quality(instance_hard, solution_rand)
