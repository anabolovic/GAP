import time
import copy
import random

from data.GapInstance import GAPInstance
from models.Agent import Agent
from models.Task import Task
from solvers.naive_solver import naive_assignment
from solvers.simulated_annealing import simulated_annealing_v2
from solvers.greedy_solver import calculate_total_cost
from visualisation.plot_assignment import plot_assignment


def generate_small_instance(num_agents=5, num_tasks=10, seed=42):
    random.seed(seed)

    agents = []
    for i in range(num_agents):
        capacity = random.randint(40, 70)  
        agents.append(Agent(i, capacity))

    tasks = []
    for t in range(num_tasks):
        costs = []
        demands = []

        for a in range(num_agents):
            costs.append(random.randint(5, 30))
            demands.append(random.randint(5, 25))

        tasks.append(Task(t, demands, costs))

    return GAPInstance(agents, tasks)


def calculate_assignment_quality(instance, assignment, label=""):
    total_cost = calculate_total_cost(instance, assignment)
    assigned_count = sum(1 for a in assignment.values() if a != -1)
    print(f"\n[{label}]")
    print(f"Ukupan trošak: {total_cost}")
    print(f"Dodeljeni zadaci: {assigned_count}/{len(assignment)}")


if __name__ == "__main__":
    instance = generate_small_instance()
    for agent in instance.agents:
        print(f"Agent {agent.id}: kapacitet = {agent.capacity}")
    print("Zadaci (trošak po agentu / zahtev po agentu):")
    for task in instance.tasks:
        print(f"Task {task.id}:")
        for a_id in range(len(instance.agents)):
            print(f"   Agent {a_id}: cost={task.costs[a_id]}, demand={task.demands[a_id]}")


    inst_naive = copy.deepcopy(instance)
    print("\n--- Naive Assignment ---")
    start_naive = time.time()
    naive_result = naive_assignment(inst_naive)
    end_naive = time.time()
    calculate_assignment_quality(inst_naive, naive_result, "Naive")
    print(f"Vreme izvršavanja: {end_naive - start_naive:.4f} sekundi")
    plot_assignment(inst_naive, naive_result, "Naive")


    inst_sa = copy.deepcopy(instance)
    print("\n--- Simulated Annealing ---")
    start_sa = time.time()
    sa_result = simulated_annealing_v2(
        inst_sa,
        initial_temp=300.0,
        min_temp=1e-3,
        max_iter=5000,
        cooling="geometric",
        alpha=0.995,
        acceptance="boltzmann",
        neighborhood="mixed",
        moves_per_step=(1, 3),
        seed=123
    )
    end_sa = time.time()
    calculate_assignment_quality(inst_sa, sa_result, "Simulated Annealing")
    print(f"Vreme izvršavanja: {end_sa - start_sa:.4f} sekundi")
    plot_assignment(inst_sa, sa_result, "Simulated Annealing")
