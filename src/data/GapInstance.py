import random
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

def create_large_test_instance() -> GAPInstance:
    agents = [
        Agent(id=0, capacity=15),
        Agent(id=1, capacity=20),
        Agent(id=2, capacity=18),
        Agent(id=3, capacity=22),
    ]

    tasks = [
        Task(id=0, demands=[3, 5, 4, 3], costs=[10, 12, 8, 9]),
        Task(id=1, demands=[6, 4, 5, 6], costs=[13, 10, 11, 14]),
        Task(id=2, demands=[5, 6, 4, 5], costs=[15, 14, 9, 13]),
        Task(id=3, demands=[4, 3, 4, 2], costs=[11, 9, 10, 8]),
        Task(id=4, demands=[3, 4, 2, 3], costs=[8, 9, 6, 7]),
        Task(id=5, demands=[7, 8, 6, 7], costs=[17, 15, 12, 16]),
        Task(id=6, demands=[5, 5, 5, 5], costs=[10, 11, 9, 13]),
        Task(id=7, demands=[2, 3, 2, 2], costs=[5, 7, 4, 6]),
    ]

    return GAPInstance(agents, tasks)


def create_tricky_instance_v2() -> GAPInstance:
    import random
    random.seed(42)

    agents = []
    tasks = []

    num_cheap_agents = 5
    num_strong_agents = 15
    total_agents = num_cheap_agents + num_strong_agents

    for i in range(num_cheap_agents):
        agents.append(Agent(id=i, capacity=30))

    for i in range(num_cheap_agents, total_agents):
        agents.append(Agent(id=i, capacity=300))

    for t_id in range(30):
        demands = []
        costs = []
        for a_id in range(total_agents):
            if a_id < num_cheap_agents:
                demands.append(5)
                costs.append(1) 
            else:
                demands.append(5)
                costs.append(100) 
        tasks.append(Task(id=t_id, demands=demands, costs=costs))

    for t_id in range(30, 50):
        demands = []
        costs = []
        for a_id in range(total_agents):
            if a_id < num_cheap_agents:
                demands.append(50)
                costs.append(999)  
            else:
                demands.append(50)
                costs.append(10 + random.randint(0, 5))
        tasks.append(Task(id=t_id, demands=demands, costs=costs))

    return GAPInstance(agents, tasks)

def create_local_search_favored_instance() -> GAPInstance:
    import random
    random.seed(123)

    agents = []
    tasks = []

    num_cheap_agents = 10
    num_strong_agents = 10
    total_agents = num_cheap_agents + num_strong_agents

    # 10 slabih agenata sa tačno 30 kapaciteta
    for i in range(num_cheap_agents):
        agents.append(Agent(id=i, capacity=30))

    # 10 jakih agenata sa 150 kapaciteta
    for i in range(num_cheap_agents, total_agents):
        agents.append(Agent(id=i, capacity=150))

    # 20 malih zadataka
    for t_id in range(20):
        demands = [5] * total_agents
        costs = [10] * total_agents  # svi izgledaju jednako dobro
        tasks.append(Task(id=t_id, demands=demands, costs=costs))

    # 10 velikih zadataka (50)
    for t_id in range(20, 30):
        demands = []
        costs = []
        for a_id in range(total_agents):
            if a_id < num_cheap_agents:
                demands.append(50)
                costs.append(999)  # fizički i ekonomski nemoguće
            else:
                demands.append(50)
                costs.append(5 + (a_id % 3))  # jefitno za jake agente
        tasks.append(Task(id=t_id, demands=demands, costs=costs))

    return GAPInstance(agents, tasks)



