from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from typing import List
from graph import Graph
from packages import Package

class Truck:
    # keep track of all truck instances
    trucks = []

    # Setup the truck with the truck ID, graph, packages, all packages, and special notes
    def __init__(self, truck_id: str, graph: Graph, packages: List[Package], all_packages: List[Package], special_notes: List[str] = None):
        self.truck_id = truck_id
        self.graph = graph
        self.packages = packages
        self.all_packages = all_packages
        self.special_notes = special_notes if special_notes else []
        # Truck capacity for packages
        self.capacity = 16
        # Truck speed miles per hour
        self.speed = 18  
        # Hub address location
        self.current_location = 'Western Governors University'
        # List to keep track of delivered packages
        self.delivered_packages = []
        # Delivery nodes set for the truck
        self.delivery_nodes = set()
        # Queue to keep track of the delivery route
        self.delivery_route = Queue()
        # Add the truck to the list of trucks
        Truck.trucks.append(self)

    # Load the package onto the truck
    def load_package(self, package: Package):
        # Set initial status to "AT HUB"
        package.delivery_status = "AT HUB"  
        # Assign the truck ID to the package
        package.truck = self.truck_id 
        # Add the package to the truck's package list
        self.packages.append(package)
        # Add the location name to delivery nodes
        self.delivery_nodes.add(package.location_name)

    # Load packages onto the truck based on package IDs
    def load_packages_by_id(self):
        # Clear the truck's package list 
        self.packages.clear()
        # Define package IDs for each truck
        truck_packages = {
            "Truck 1": [15, 16, 13, 14, 20, 21, 29, 19, 17, 24, 30, 31, 1, 22],
            "Truck 2": [40, 37, 34, 7, 11, 23, 27, 36, 38, 18, 3, 26, 6, 25],
            "Truck 3": [9, 28, 32, 2, 5, 10, 12, 35, 39, 33, 8, 4]
        }

        # Get the package IDs for the current truck
        current_truck_packages = truck_packages.get(self.truck_id, [])
        # Load packages based on the package IDs
        for package_id in current_truck_packages:
            package = next((pkg for pkg in self.all_packages if pkg.package_id == package_id and not pkg.loaded), None)
            # Load the package if it is not already loaded
            if package and len(self.packages) < self.capacity:
                self.load_package(package)
                package.loaded = True
        print(f"Final packages for {self.truck_id}: {[pkg.package_id for pkg in self.get_packages()]}")
    
    # Get the packages on the truck
    def get_packages(self):
        return self.packages

    # Get the packages currently being delivered
    def get_packages_currently_being_delivered(self, location_name):
        return [package for package in self.packages if package.location_name == location_name]

    # Get the truck ID and the number of packages remaining
    def __str__(self):
        return f"Truck {self.truck_id} has {len(self.packages)} packages remaining."

    # Remove a package from the truck
    def remove_package(self, package):
        # Remove the package from the truck's package list
        if package in self.packages:
            # Remove the package from the truck's package list
            self.packages.remove(package)
            # Remove the location name from delivery nodes
            self.delivery_nodes.discard(package.location_name)

    # Update a package on the truck
    def update_package(self, updated_package: Package):
        for i, pkg in enumerate(self.packages):
            # Update the package if the package ID matches
            if pkg.package_id == updated_package.package_id:
                self.packages[i] = updated_package
                self.delivery_nodes.add(updated_package.location_name)
                return True
        return False

    # Get all packages on board the truck
    def get_all_packages_on_board(self):
        return [pkg.package_id for pkg in self.packages]

    # Deliver packages based on the delivery route
    def deliver_packages(self, departure_time, package_setup, package_status_over_time, package_9_has_been_updated, combined_total_distance, current_packages):
        # Setup package statuses
        self.setup_package_status(package_status_over_time, departure_time)
        in_transit_begin = departure_time.strftime("%H:%M:%S")
        drive_distance = 0
        dont_ask_to_update_9 = False
        delivery_process = []
        current_locations = []
        return_time = departure_time 

        # Deliver packages based on the delivery route
        while not self.delivery_route.empty():
            next_delivery = self.delivery_route.get()
            current_location = next_delivery[0]
            distance_to_next = float(next_delivery[1])
            current_packages = self.get_packages_currently_being_delivered(current_location)

            # Update time and distance for the trip
            time_spent = timedelta(hours=distance_to_next / self.speed)
            departure_time += time_spent
            drive_distance += distance_to_next  # Increment drive_distance for the truck
            combined_total_distance[0] += distance_to_next  # Update combined total distance

            if self.should_update_package_9(departure_time, package_9_has_been_updated, dont_ask_to_update_9):
                package_9_has_been_updated, dont_ask_to_update_9 = self.update_package_9(package_setup, current_packages)
                # Recalculate the delivery route if package 9 is updated
                self.graph.start_delivery_route(self.delivery_nodes, self.current_location)

            # Correct the method call here
            for package in current_packages:
                package_setup.update_package_status(package.package_id, "DELIVERED", departure_time)
                if package.package_id in package_status_over_time:
                    package_status_over_time[package.package_id].append((departure_time.time(), "DELIVERED"))
                else:
                    package_status_over_time[package.package_id] = [(departure_time.time(), "DELIVERED")]
                self.remove_package(package)

            # Mark all packages as "IN TRANSIT" after the start of delivery
            for package in self.packages:
                if package.delivery_status != "DELIVERED":  # Ensure not to update already delivered packages
                    # Check if the truck is at the hub or at the package's delivery location
                    if self.current_location == 'Western Governors University':
                        package.delivery_status = "AT HUB"
                        package_setup.update_package_status(package.package_id, "AT HUB", departure_time)
                    elif self.current_location == package.location_name:
                        package.delivery_status = "DELIVERED"
                        package_setup.update_package_status(package.package_id, "DELIVERED", departure_time)
                    else:
                        package.delivery_status = "IN TRANSIT"
                        package_setup.update_package_status(package.package_id, "IN TRANSIT", departure_time)
                    
                    # Update the package status over time
                    if package.package_id in package_status_over_time:
                        package_status_over_time[package.package_id].append((departure_time.time(), package.delivery_status))
                    else:
                        package_status_over_time[package.package_id] = [(departure_time.time(), package.delivery_status)]
            
            # Update package status based on truck location
            for package in self.packages:
                package_setup.update_package_status(package.package_id, package.delivery_status, package.delivery_time)

            self.current_location = current_location

            delivery_status = self.print_delivery_status(departure_time, next_delivery, drive_distance, combined_total_distance[0], package_id=current_packages)
            delivery_process.append(delivery_status)
            current_locations.append((departure_time, current_location))
            sleep(.5)
        # Calculate return trip to the hub
        if self.current_location != "Western Governors University":
            return_distance = self.graph.return_to_hub(self.current_location)
            drive_distance += return_distance
            combined_total_distance[0] += return_distance
            return_time = departure_time + timedelta(hours=return_distance / self.speed)
            # Print return trip status without updating package statuses
            return_trip_status = self.print_delivery_status(return_time, ['Western Governors University', return_distance], drive_distance, combined_total_distance[0], package_id=None)
            delivery_process.append(return_trip_status)
            current_locations.append((return_time, 'Western Governors University'))

        # Filter out duplicate statuses
        for package_id, statuses in package_status_over_time.items():
            seen_statuses = set()
            unique_statuses = []
            for time, status in statuses:
                # Only add unique statuses
                if status not in seen_statuses:
                    unique_statuses.append((time, status))
                    seen_statuses.add(status)
            # Update the package status over time
            package_status_over_time[package_id] = unique_statuses

        return [return_time, drive_distance / self.speed, drive_distance, package_9_has_been_updated, delivery_process, current_locations]

    # Print the delivery status for the truck
    def print_delivery_status(self, current_time, next_delivery, truck_total_distance, combined_total_distance, package_id):
        # Get all package IDs on board
        all_package_ids = self.get_all_packages_on_board()
        # Extract current package IDs
        current_package_ids = [pkg.package_id for pkg in package_id]  
        # Extract current package locations
        current_package_locations = [pkg.location_name for pkg in package_id]  

        # Print the return status for the truck packages
        if next_delivery[0] == 'Western Governors University':
            status = (f"\t{current_time.strftime('%H:%M:%S')}: {self.truck_id} Returning to: '{next_delivery[0]}'\n"
                    f"\tTotal distance traveled by {self.truck_id}: {truck_total_distance:.2f} miles\n"
                    f"\tCombined total distance of all trucks: {combined_total_distance:.2f} miles\n"
                    f"\tUpdated truck packages left: {all_package_ids}\n")
            print(status)
            return status
        # Print the delivery status for the truck
        elif current_package_ids and current_package_locations:
            status = (f"\t{current_time.strftime('%H:%M:%S')}: {self.truck_id} Delivering packages {current_package_ids} to {current_package_locations}\n"
                    f"\tAll packages on board: {all_package_ids}\n"
                    f"\tTotal distance traveled by {self.truck_id}: {truck_total_distance:.2f} miles\n"
                    f"\tCombined total distance of all trucks: {combined_total_distance:.2f} miles\n"
                    f"\tUpdated truck packages left: {all_package_ids}\n")
            print(status)
            return status
        return ""

    # Setup the package status for the truck
    def setup_package_status(self, package_status_over_time, departure_time):
        for pkg in self.packages:
            package_status_over_time[pkg.package_id] = [(departure_time.time(), "AT HUB")]

    # Check if package #9 for Truck 3 should be updated
    def should_update_package_9(self, current_time, package_9_has_been_updated, dont_ask_to_update_9):
        ten_twenty_am = datetime(2021, 7, 1, 10, 20, 0)
        return current_time >= ten_twenty_am and not package_9_has_been_updated and self.truck_id == "Truck 3" and not dont_ask_to_update_9

    # Update package #9 for Truck 3 to the correct address if user chooses
    def update_package_9(self, package_setup, current_packages):
        # Only update package #9 for Truck 3
        if self.truck_id != "Truck 3":
            return False, False  
        print("Currently it is 10:20, there is an update to package #9!")
        print("Correct package #9? Enter 'yes' or 'no'")
        answer = input(">")
        while answer not in ("yes", "no"):
            print("Invalid Response. 'yes' or 'no' correct the address for package #9? Enter 'yes' or 'no'")
            answer = input(">")
        # User decided to update the package # 9
        if answer == "yes":
            # Update the package #9 address
            updated_package = Package(9, "Third District Juvenile Court", "410 S State St", "Salt Lake City", "UT", "84111", "EOD", 5, "AT HUB")
            # Ensure the truck ID is set
            updated_package.truck = self.truck_id 
            print(f"Inserting updated package: {updated_package}")
            # Update the package in the package_setup.py
            package_setup.update_package(updated_package)
            print("Package #9's address is now 410 S State St. Salt Lake City, UT 84111.")
        # User decided not to update the package # 9
        else:
            updated_package = Package(9, "Council Hall", "300 State St", "Salt Lake City", "UT", "84103", "EOD", 2, "Wrong address listed")
            # Ensure the truck ID is set
            updated_package.truck = self.truck_id
            print(f"Inserting updated package: {updated_package}")
            # Update the package in the package_setup.py
            package_setup.update_package(updated_package)
        # Ensure the updated package is added to the truck's package list
        if updated_package.package_id not in [pkg.package_id for pkg in self.packages]:
            self.packages.append(updated_package)
            self.delivery_nodes.add(updated_package.location_name)
        sleep(1)
        return True, False if answer == "yes" else False