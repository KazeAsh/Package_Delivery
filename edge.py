import csv

class Edge:
    # Edge class to represent a connection between two nodes
    def __init__(self, from_node, to_node, weight):
        # Setup the edge with a from_node, to_node, and weight
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    
    # Define the string representation of the edge
    def __repr__(self) -> str:
        return f"Edge({self.from_node}, {self.to_node}, {self.weight})"