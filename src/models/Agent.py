class Agent:
    def __init__(self, id: int, capacity: int):
        self.id = id
        self.capacity = capacity
        self.remaining_capacity = capacity

    def __str__(self):
        return f"Agent {self.id} | Capacity: {self.capacity}"
    
    def reset(self):
        self.remaining_capacity = self.capacity