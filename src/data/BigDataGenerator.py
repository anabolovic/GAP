import random
from data.GapInstance import GAPInstance
from models.Agent import Agent
from models.Task import Task


def generate_hard_instance(num_agents=30, num_tasks=300, seed=42):
    random.seed(seed)

    agents = []
    for i in range(num_agents):
        capacity = random.randint(100, 200)
        agents.append(Agent(i, capacity))

    tasks = []
    for t in range(num_tasks):
        costs = []
        demands = []

        for a in range(num_agents):

            if a < 3:
                costs.append(random.randint(1, 5))
                demands.append(random.randint(30, 50))
            else:
                costs.append(random.randint(40, 100))
                demands.append(random.randint(5, 20))


        tasks.append(Task(t, demands, costs))

    return GAPInstance(agents, tasks)
