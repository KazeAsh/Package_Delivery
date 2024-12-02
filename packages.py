from typing import Optional
import csv

class Package:
    # Package class to represent a package
    def __init__(self, package_id: int, location_name: str, address: str, city: str, state: str, zip_code: str, deadline: str, weight: float, special_notes: Optional[str] = None, delivery_status: str = "AT THE HUB", delivery_time: Optional[str] = None):
        # Setup the package with the package necessary information need to
        #track the package or deliver the package
        self.package_id = package_id
        self.location_name = location_name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes if special_notes is not None else []
        self.delivery_status = delivery_status
        self.delivery_time = delivery_time
        self.departure_time = None
        self.delivery_address = address
        self.loaded = False
        self.truck = None  

    # Set status using the delivery status
    def set_status(self, status: str):
        self.delivery_status = status

    # Get the status of the package
    def get_status(self):
        return self.delivery_status

    # Check if two Package objects are equal
    def __eq__(self, other):
        if isinstance(other, Package):
            return (self.package_id == other.package_id and
                    self.location_name == other.location_name and
                    self.address == other.address and
                    self.city == other.city and
                    self.state == other.state and
                    self.zip_code == other.zip_code and
                    self.deadline == other.deadline and
                    self.weight == other.weight and
                    self.special_notes == other.special_notes and
                    self.delivery_status == other.delivery_status and
                    self.delivery_time == other.delivery_time)
        return False

    # repr method to represent the package object
    def __repr__(self):
        return (f"Package({self.package_id}, {self.location_name}, {self.address}, {self.city}, "
                f"{self.state}, {self.zip_code}, {self.deadline}, {self.weight}, {self.delivery_status})")