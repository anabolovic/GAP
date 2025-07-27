from data.GapInstance import GAPInstance
from typing import Optional

def greedy_assignment(instance: GAPInstance) -> dict[int, int]:
    """
    Vraća rešenje kao dict: {task_id: agent_id}
    """
    assignment = {}

    for task in instance.tasks:
        best_agent_id: Optional[int] = None
        best_cost = float('inf')

        for agent in instance.agents:
            agent_id = agent.id
            demand = task.demands[agent_id]
            cost = task.costs[agent_id]

            if agent.remaining_capacity >= demand:
                if cost < best_cost:
                    best_cost = cost
                    best_agent_id = agent_id

        if best_agent_id is not None:
            assignment[task.id] = best_agent_id
            selected_agent = instance.agents[best_agent_id]
            selected_agent.remaining_capacity -= task.demands[best_agent_id]
        else:
            assignment[task.id] = -1  

    return assignment

def calculate_total_cost(instance: GAPInstance, assignment: dict[int, int]) -> int:
    total_cost = 0
    for task in instance.tasks:
        agent_id = assignment.get(task.id, -1)
        if agent_id != -1:
            total_cost += task.costs[agent_id]
    return total_cost