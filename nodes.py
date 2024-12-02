from typing import List
from edge import Edge

class Node:
    # Node class to represent a location in the graph
    def __init__(self, value: str):
        self.value = value
        # Sore a List of Edge objects
        self.edges: List[Edge] = []
        self.visited = False

    # Append and add Edge object to the list
    def add_edge(self, edge: Edge):
        self.edges.append(edge)  

    # Get the list of edges
    def get_edges(self) -> List[Edge]:
        return self.edges

    # Create a hash value for the Node object
    def __hash__(self):
        return hash(self.value)

    # Create eq method to compare Node objects
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.value == other.value
        return False

    def __repr__(self) -> str:
        return f"Node({self.value})"