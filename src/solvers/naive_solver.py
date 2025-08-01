from data.GapInstance import GAPInstance

def naive_assignment(instance: GAPInstance) -> dict[int, int]:
    assignment = {}

    for task in instance.tasks:
        assigned = False
        for agent in instance.agents:
            agent_id = agent.id
            demand = task.demands[agent_id]

            if agent.remaining_capacity >= demand:
                agent.remaining_capacity -= demand
                assignment[task.id] = agent_id
                assigned = True
                break 
        if not assigned:
            assignment[task.id] = -1 

    return assignment
