import csv
import networkx as nx
from nodes import Node
from edge import Edge
from queue import Queue
import sys

class Graph:
    def __init__(self):
        # Setup the graph with empty data structures
        self.location_names = []
        self.adjacency_matrix = []
        self.nodes = {}
        self.edges = []
        self.graph = nx.Graph()

    # Setup/Take the location names in the CSV files and store them
    def setup_location_name_data(self):
        # Load location names from a CSV file
        with open("data/WGUPS_Addresses.csv") as file:
            names_reader = csv.reader(file)
            # Skip header
            next(names_reader)  
            # Read each row and append the location name to the list
            for entry in names_reader:
                # choose to append location name [1] since it is in the second column
                self.location_names.append(entry[1]) 

    # Setup/Take distance data from the CSV file and store them
    def setup_location_distance_data(self):
        # Load distance data from a CSV file and create an adjacency matrix
        with open("data/WGUPS_Distance_Table.csv") as file:
            reader = csv.reader(file, delimiter=',')  
            # Store the adjacency matrix as a list of lists
            self.adjacency_matrix = []
            # Skip header row
            next(reader)  
            # Read each row and append to the adjacency matrix
            for row in reader:
                # Setup to Store the filtered row to the adjacency matrix
                filtered_row = []
                # Skip the first column row header
                for value in row[1:]:
                    try:
                        filtered_row.append(float(value))
                    # Handle non-numeric values
                    except ValueError:
                        filtered_row.append(0.0)
                # Append the filtered row to the adjacency matrix
                self.adjacency_matrix.append(filtered_row)
        
        # Check the adjacency matrix is square and matches the number of location names
        num_locations = len(self.location_names)
        # by checking adjacency matrix is less than the number of locations
        if len(self.adjacency_matrix) < num_locations:
            for _ in range(num_locations - len(self.adjacency_matrix)):
                self.adjacency_matrix.append([0.0] * num_locations)
        # Ensure each row in the adjacency matrix has the same number of columns
        for row in self.adjacency_matrix:
            if len(row) < num_locations:
                row.extend([0.0] * (num_locations - len(row)))

    # Setup the nodes hash table
    def setup_nodes_hash_table(self):
        # Load nodes from a CSV file 
        self.nodes = self.load_nodes("data/WGUPS_Addresses.csv")
        self.location_names = list(self.nodes.keys())
        # Storing the adjacency matrix as a list 
        self.setup_location_distance_data()
        
        # Manually add any missing nodes
        missing_nodes = ["Western Governors University"]
        for node in missing_nodes:
            if node not in self.nodes:
                self.nodes[node] = Node(node)
                # Ensure it's added to location_names
                self.location_names.append(node)  
        # Add edges to the graph to the adjacency matrix
        self.add_edges_from_adjacency_matrix()

    # Calculate the distance between two nodes using the adjacency matrix
    def distance_between(self, from_node, to_node):
        # Find the index of the nodes in the location names list 
        try:
            from_index = self.location_names.index(from_node)
        except ValueError:
            print(f"Error: '{from_node}' not found in location_names")
            return None
        # Find the index of the nodes in the location names list
        try:
            to_index = self.location_names.index(to_node)
        except ValueError:
            print(f"Error: '{to_node}' not found in location_names")
            return None
        # Get the distance from the adjacency matrix
        distance = self.adjacency_matrix[from_index][to_index]
        # Return the distance
        return distance
    
    # Add a node to the graph if it doesn't already exist
    def add_node(self, node):
        if node.value not in self.nodes:
            self.nodes[node.value] = node

    # Load nodes from a CSV file
    def load_nodes(self, file_path):
        # create a dictionary of nodes from a CSV file
        nodes = {}
        # Load nodes from a CSV file
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            # Skip header
            next(reader)  
            # Read each row and create a node
            for row in reader:
                # Assuming location name is in the second column
                location = row[1]  
                # Create a node into the dictionary
                nodes[location] = Node(location)
        return nodes

    def add_edges_from_adjacency_matrix(self):
        # Add edges to the graph based on the adjacency matrix
        for from_index, from_vertex in enumerate(self.location_names):
            for to_index, distance in enumerate(self.adjacency_matrix[from_index]):
                if distance > 0:
                    from_node = self.nodes[from_vertex]
                    to_node = self.nodes[self.location_names[to_index]]
                    edge = Edge(from_node, to_node, distance)
                    self.edges.append(edge)
                    # Add edge to the from_node
                    from_node.edges.append(edge)  
                    # Add reverse edge
                    reverse_edge = Edge(to_node, from_node, distance)
                    self.edges.append(reverse_edge)
                    # Add reverse edge to the to_node
                    to_node.edges.append(reverse_edge)  
                    self.graph.add_edge(from_vertex, self.location_names[to_index], weight=distance)

    # Calculate the distance between two locations
    def calculate_distance(self, location1, location2):
        return self.distance_between(location1, location2)

    # Start the delivery route using the Algorithm: Nearest Neighbor
    def start_delivery_route(self, delivery_nodes, current_location):
        # Setup the current node as the starting location
        current_node = current_location
        # Create a queue to store the delivery route
        delivery_route = Queue()
        # Setup the total distance to 0
        total_distance = 0
        # Convert the list of delivery nodes to a set for faster lookup
        nodes_remaining = set(delivery_nodes)
            
        # Loop until all nodes have been visited
        while nodes_remaining:
            # Find the edges for the current node
            edges = next((node.edges for node in self.nodes.values() if node.value == current_node), None)
            # If no edges are found for the current node, print an error message and return default values
            if edges is None:
                print(f"Error: No node found with name {current_node}")
                # Return default values to avoid crashing
                return 0, delivery_route  
            
            # Setup the shortest distance to a very large number
            shortest_distance = sys.maxsize
            next_node_for_delivery_route = None
            # Iterate over the edges to find the nearest neighbor
            for edge in edges:
                if edge.to_node.value in nodes_remaining:
                    if float(edge.weight) < shortest_distance:
                        shortest_distance = float(edge.weight)
                        next_node_for_delivery_route = [edge.to_node.value, edge.weight]
            
            # If no valid next node is found, print an error message and return default values
            if next_node_for_delivery_route is None:
                print(f"Error: No valid next node found from {current_node}. Check the graph for connectivity issues.")
                # Return default values to avoid crashing
                return 0, delivery_route  

            # Move to the next closest node
            current_node = next_node_for_delivery_route[0]
            # Remove the current node from the set of remaining nodes
            nodes_remaining.discard(current_node)
            # Add the distance to the total distance
            total_distance += shortest_distance
            # Add the next node to the delivery route
            delivery_route.put(next_node_for_delivery_route)

        # Add the return trip to the hub
        return_distance = self.return_to_hub(current_node)
        total_distance += return_distance
        delivery_route.put(["Western Governors University", return_distance])
        # Return the total distance and the delivery route
        return total_distance, delivery_route

    # Return to the hub from the current node
    def return_to_hub(self, current_node):
        hub_node = "Western Governors University"        
        # Check if the current node is already the hub
        if current_node == hub_node:
            return 0.0
        # Find the edge weight from the current node to the hub
        for node in self.nodes.values():
            if node.value == current_node:
                for edge in node.edges:
                    if edge.to_node.value == hub_node:
                        return float(edge.weight)
        # Raise an error if no path is found from the current node to the hub
        raise ValueError(f"No path found from {current_node} to the hub")