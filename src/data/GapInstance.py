from models.Agent import Agent
from Task import Task


class GAPInstance:
    def __init__(self, agents: list[Agent], tasks: list[Task]): # type: ignore
        self.agents = agents
        self.tasks = tasks

    def __str__(self):
        agent_str = "\n".join(str(agent) for agent in self.agents)
        task_str = "\n\n".join(str(task) for task in self.tasks)
        return f"--- Agents ---\n{agent_str}\n\n--- Tasks ---\n{task_str}"

def create_test_instance() -> GAPInstance:
    agents = [
        Agent(id=0, capacity=10),
        Agent(id=1, capacity=15),
        Agent(id=2, capacity=12),
    ]

    tasks = [
        Task(id=0, demands=[4, 5, 3], costs=[12, 15, 9]),
        Task(id=1, demands=[6, 4, 5], costs=[10, 13, 8]),
        Task(id=2, demands=[5, 6, 4], costs=[11, 14, 7]),
        Task(id=3, demands=[3, 5, 4], costs=[9, 10, 6]),
        Task(id=4, demands=[4, 5, 3], costs=[13, 12, 8]),
    ]

    return GAPInstance(agents, tasks)
