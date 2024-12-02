class Driver:
    # Driver class to represent a driver
    # Class attribute to store the total number of drivers
    total_drivers = 0

    # Setup the driver with an id and a truck
    def __init__(self, driver_id):
        self.id = driver_id
        # Set the truck to None initially
        self.truck = None
        # Increment the total number of drivers
        Driver.total_drivers += 1

    # Assign a truck to the driver
    def assign_truck(self, truck):
        self.truck = truck
    
