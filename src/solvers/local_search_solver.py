from data.GapInstance import GAPInstance
from solvers.greedy_solver import greedy_assignment, calculate_total_cost
import copy


def local_search_assignment(instance: GAPInstance) -> dict[int, int]:
    # Kopiramo instancu da ne kvarimo original (jer greedy menja kapacitete)
    instance = copy.deepcopy(instance)
    assignment = greedy_assignment(instance)

    improved = True
    while improved:
        improved = False
        for task1 in instance.tasks:
            for task2 in instance.tasks:
                if task1.id == task2.id:
                    continue

                a1 = assignment.get(task1.id, -1)
                a2 = assignment.get(task2.id, -1)

                if a1 == -1 or a2 == -1 or a1 == a2:
                    continue

                # trenutni agenti
                agent1 = instance.agents[a1]
                agent2 = instance.agents[a2]

                # Zahtevi ako se zamene
                d1_new = task1.demands[a2]
                d2_new = task2.demands[a1]
                d1_old = task1.demands[a1]
                d2_old = task2.demands[a2]

                # Proveri da li novi agenti mogu da izvrše zadatke
                if (
                    agent1.remaining_capacity + d1_old >= d2_new and
                    agent2.remaining_capacity + d2_old >= d1_new
                ):
                    old_cost = task1.costs[a1] + task2.costs[a2]
                    new_cost = task1.costs[a2] + task2.costs[a1]

                    if new_cost < old_cost:
                        # oslobodi stare kapacitete
                        agent1.remaining_capacity += d1_old
                        agent2.remaining_capacity += d2_old
                        # rezerviši nove
                        agent1.remaining_capacity -= d2_new
                        agent2.remaining_capacity -= d1_new
                        # ažuriraj assignment
                        assignment[task1.id] = a2
                        assignment[task2.id] = a1
                        improved = True

    return assignment


def calculate_assignment_quality(instance: GAPInstance, assignment: dict[int, int]) -> None:
    total_cost = calculate_total_cost(instance, assignment)
    assigned_count = sum(1 for a in assignment.values() if a != -1)
    print(f"Ukupan trošak: {total_cost}")
    print(f"Dodeljeni zadaci: {assigned_count}/{len(assignment)}")
