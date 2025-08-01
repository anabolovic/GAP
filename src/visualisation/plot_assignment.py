import matplotlib.pyplot as plt
from data.GapInstance import GAPInstance
from collections import defaultdict

def plot_assignment(instance: GAPInstance, assignment: dict[int, int], title: str):
    agent_loads = defaultdict(list)  # agent_id → list of (task_id, demand)

    for task in instance.tasks:
        agent_id = assignment.get(task.id, -1)
        if agent_id != -1:
            demand = task.demands[agent_id]
            agent_loads[agent_id].append((task.id, demand))

    fig, ax = plt.subplots()

    bottom = [0] * len(instance.agents)
    agent_ids = [agent.id for agent in instance.agents]

    for task_id in range(len(instance.tasks)):
        heights = []
        for i, agent in enumerate(instance.agents):
            load = next((d for t_id, d in agent_loads[agent.id] if t_id == task_id), 0)
            heights.append(load)

        bars = ax.bar(agent_ids, heights, bottom=bottom, label=f"Task {task_id}")
        bottom = [b + h for b, h in zip(bottom, heights)]

    capacities = [agent.capacity for agent in instance.agents]
    ax.plot(agent_ids, capacities, 'r--', label='Kapacitet')

    ax.set_xlabel("Agent ID")
    ax.set_ylabel("Zauzeće kapaciteta")
    ax.set_title(title + " Assignment Vizualizacija")
    ax.legend()
    plt.tight_layout()
    plt.show()
