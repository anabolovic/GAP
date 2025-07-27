class Task:
    def __init__(self, id: int, demands: list[int], costs: list[int]):
        self.id = id
        self.demands = demands
        self.costs = costs

    def __str__(self):
        cost_demand_str = "\n".join(
            [f"\tAgent {i} → Cost: {self.costs[i]}, Demand: {self.demands[i]}" for i in range(len(self.costs))]
        )
        return f"Task {self.id}:\n{cost_demand_str}"
