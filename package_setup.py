from hash_table import HashTable
from packages import Package
from trucks import Truck
import csv
from typing import Optional

class PackageSetup:
    # PackageSetup class to setup and manage packages
    def __init__(self, file_path="data/WGUPS_Package_File.csv"):
        self.TOTAL_PACKAGES = 40
        self.packages = {}
        self.packages_hash_table = HashTable()
        self.setup_packages_from_csv(file_path)

    # Get the packages dictionary
    def __iter__(self):
        return iter([package for id, package in self.packages.items()])

    # Get the length of the packages dictionary
    def __len__(self):
        return len(self.packages)
    
    # Insert a package into the dictionary and hash table
    def insert(self, item):
        self.packages[item.package_id] = item
        self.packages_hash_table.insert(item.package_id, item)  

    # Setup the packages from a CSV file
    def setup_packages_from_csv(self, file_path):
        location_address_to_names = HashTable()
        # Load location names from the CSV file
        with open("data/WGUPS_Addresses.csv") as file:
            names_reader = csv.reader(file)
            raw_distance_names = list(names_reader)
            for entry in raw_distance_names:
                location_address_to_names.insert(entry[2], entry[1])

        # Load package data from a CSV file
        with open(file_path) as file:
            packages_reader = csv.reader(file)
            raw_package_data = list(packages_reader)

        # Skip the header row
        raw_package_data = raw_package_data[1:]

        for entry in raw_package_data:
            if len(entry) > 1:
                location_name = location_address_to_names.get(entry[1])
                # Fallback to the original address if not found in the hash table
                if location_name is None:
                    location_name = entry[1]  
                package = Package(
                    package_id=int(entry[0]), 
                    location_name=location_name,
                    address=entry[1],
                    city=entry[2],
                    state=entry[3],
                    zip_code=entry[4],
                    deadline=entry[5],  
                    weight=float(entry[6]),  
                    special_notes=entry[7],
                    delivery_status="AT THE HUB"
                )
             # Use the insert package to both the dictionary and the hash table
                self.insert(package) 

    # Get a package by its ID
    def get_package_by_id(self, id):
        return self.packages_hash_table.get(int(id))

    # Remove a package by its ID
    def remove_package_by_id(self, id):
        package = self.packages.pop(int(id), None)
        if package:
            self.packages_hash_table.remove(int(id))
        return package

    # Get packages by address
    def get_packages_by_address(self, address):
        return [self.get_package_by_id(id) for id in range(1, self.TOTAL_PACKAGES + 1) if self.get_package_by_id(id).delivery_address == address]

    # Get packages by city
    def get_packages_by_city(self, city):
        return [self.get_package_by_id(id) for id in range(1, self.TOTAL_PACKAGES + 1) if self.get_package_by_id(id).delivery_city == city]

    # Get packages by deadline
    def get_packages_by_deadline(self, deadline):
        return [self.get_package_by_id(id) for id in range(1, self.TOTAL_PACKAGES + 1) if self.get_package_by_id(id).deadline == deadline]

    # Get packages by zip
    def get_packages_by_zip(self, zip):
        return [self.get_package_by_id(id) for id in range(1, self.TOTAL_PACKAGES + 1) if self.get_package_by_id(id).delivery_zip == zip]

    # Get packages by weight
    def get_packages_by_weight(self, weight):
        return [self.get_package_by_id(id) for id in range(1, self.TOTAL_PACKAGES + 1) if self.get_package_by_id(id).weight == weight]

    # Get packages by status
    def get_packages_by_status(self, status):
        return [self.get_package_by_id(id) for id in range(1, self.TOTAL_PACKAGES + 1) if self.get_package_by_id(id).delivery_status == status]

    # Get packages by special notes
    def get_packages_by_special_notes(self, special_notes):
        return [self.get_package_by_id(id) for id in range(1, self.TOTAL_PACKAGES + 1) if self.get_package_by_id(id).special_notes == special_notes]
    
    # Get all packages in the dictionary
    def get_all_packages(self):
        return list(self.packages.values())
    
    # Get the packages assigned to a truck by truck ID
    def get_packages_by_truck_id(self, truck_id):
        return [package for package in self.packages.values() if package.truck == truck_id]

    # Get the status of a package by its ID
    def get_package_status(self, package_id):
        package = self.get_package_by_id(package_id)
        if package:
            return package.delivery_status
        return None

    # Update the package status based on the truck's location vs package address
    def update_package_status(self, package_id, status, delivery_time=None):
        package = self.get_package_by_id(package_id)
        if package:
            # If the package is already delivered, do not change its status
            if package.delivery_status == "DELIVERED":
                return

            # Check if the truck is at the hub or at the package's delivery location
            truck = next((truck for truck in Truck.trucks if truck.truck_id == package.truck), None)
            if truck:
                # Update to Deliver if the current location matches package location name
                if truck.current_location == package.location_name:
                    package.delivery_status = "DELIVERED"
                    if delivery_time:
                        package.delivery_time = delivery_time
                # Update to At Hub if the current location is the hub
                elif truck.current_location == 'Western Governors University' and package.delivery_status != "DELIVERED":
                    package.delivery_status = "AT HUB"
                    if delivery_time:
                        package.delivery_time = delivery_time
                # Update to In Transit if the truck is not at hub or package location_name
                else:
                    package.delivery_status = "IN TRANSIT"
                    if delivery_time:
                        package.delivery_time = delivery_time
            # If the truck is not found, update the package status
            else:
                package.delivery_status = status
                if delivery_time:
                    package.delivery_time = delivery_time

            # Ensure the truck assignment is updated
            package.truck = truck.truck_id if truck else package.truck

            # Update the package in the dictionary
            self.packages[package_id] = package  
            # Ensure the updated package is saved back to the hash table
            self.packages_hash_table.insert(package_id, package) 

    # Update the package in the dictionary and hash table        
    def update_package(self, package: Package):
        self.packages[package.package_id] = package
        self.packages_hash_table.insert(package.package_id, package)

        print(f"Package #{package.package_id} has been updated.")
        # Goes through all trucks and updates the package if it's found
        for truck in Truck.trucks:
            for i, pkg in enumerate(truck.packages):
                if pkg.package_id == package.package_id:
                    truck.packages[i] = package
