import random


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
