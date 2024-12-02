# Ashley Pilger Student ID:011622730

import tkinter as tk
from tkinter import ttk
from package_setup import PackageSetup
from graph import Graph
from trucks import Truck
from driver import Driver
from datetime import datetime, timedelta

# Create a UI class to display the delivery system
class DeliverySystemUI:
    # Setup/Initialize the UI with the root window
    def __init__(self, root):
        self.root = root
        self.root.title("WGUPS Package Delivery System")

        # Setup package setup and load packages from CSV
        self.package_setup = PackageSetup()
        self.package_setup.setup_packages_from_csv("data/WGUPS_Package_File.csv")
        self.all_packages = self.package_setup.get_all_packages()

        # Used for storing package status over time
        self.package_status_over_time = {}
        
        # Setup the graph and setup location data
        self.graph = Graph()
        self.graph.setup_location_name_data()
        self.graph.setup_location_distance_data()
        self.graph.setup_nodes_hash_table()

        # Initialize trucks with the graph and all packages
        self.truck1 = Truck("Truck 1", self.graph, [], self.all_packages)
        self.truck2 = Truck("Truck 2", self.graph, [], self.all_packages)
        self.truck3 = Truck("Truck 3", self.graph, [], self.all_packages)

        # Initialize drivers and assign them to trucks
        self.driver1 = Driver("Driver 1")
        self.driver2 = Driver("Driver 2")
        self.driver1.assign_truck(self.truck1)
        self.driver2.assign_truck(self.truck2)

        # Create the main menu
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(pady=30)

        # Add buttons to the main menu
        tk.Button(frame, text="Delivery Menu", command=self.create_delivery_screen).pack(pady=10)
        tk.Button(frame, text="Today's Packages", command=self.create_package_lookup_screen).pack(pady=10)
        tk.Button(frame, text="Quit", command=self.root.quit).pack(pady=10)

    # Create the delivery screen
    def create_delivery_screen(self):
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(pady=30)

        # Add buttons to the delivery screen
        tk.Button(self.root, text="Start Delivery", command=self.start_delivery).pack()
        tk.Button(self.root, text="Check Status by Time", command=self.show_time_frames).pack(pady=10)
        tk.Button(self.root, text="Search Package", command=self.search_package_id).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu).pack(pady=10)
        
        # Create a frame to hold the text box and scrollbar
        text_frame = tk.Frame(self.root)
        text_frame.pack(pady=10)

        # Create the text box with larger dimensions
        self.log_text = tk.Text(text_frame, height=30, width=100, wrap=tk.NONE)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the scrollbar and attach it to the text box
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Create a progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=10)

    # Create a screen to look up the package
    def create_package_lookup_screen(self):
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(pady=30)

        # Create a text box to display package information
        self.package_info_text = tk.Text(frame, height=50, width=100, wrap=tk.NONE)
        self.package_info_text.grid(row=0, column=0, padx=10, pady=10)

        # Create a scrollbar and attach it to the text box
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.package_info_text.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.package_info_text.config(yscrollcommand=scrollbar.set)

        # Add a button to go back to the main menu
        tk.Button(frame, text="Back to Main Menu", command=self.create_main_menu).grid(row=1, column=0, columnspan=2, pady=10)
        self.display_all_packages()

    # Display a lookup package system using time to show details of each package
    def lookup_package(self, start_time_str, end_time_str):
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(pady=30)

        # Convert the time strings to time objects
        start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
        end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()

        # Create a text box to display package statuses
        self.log_text = tk.Text(frame, height=30, width=100, wrap=tk.NONE)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar and attach it to the text box
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Display package statuses within the time frame
        for package_id, statuses in self.package_status_over_time.items():
            info = f"Package ID: {package_id}\n"
            last_status = None
            for time, status in statuses:
                status_time = time  # Directly use the time object
                if start_time <= status_time <= end_time:
                    if status != last_status:
                        info += f"Time: {time.strftime('%H:%M:%S')}, Status: {status}\n"
                        last_status = status
            info += "----------------------\n"
            self.log_text.insert(tk.END, info)

        # Add a button to go back to the time frames screen
        tk.Button(frame, text="Back to Time Frames", command=self.show_time_frames).pack(pady=10)

    # Display all package information
    def display_all_packages(self):
        self.package_info_text.delete(1.0, tk.END)
        # Display package information in the text box
        for package in self.all_packages:
            info = (
                f"ID: {package.package_id}\n"
                f"Address: {package.address}\n"
                f"Deadline: {package.deadline}\n"
                f"City: {package.city}\n"
                f"Zip Code: {package.zip_code}\n"
                f"Weight: {package.weight}\n"
                f"Status: {package.delivery_status}\n"
                "----------------------\n"
            )
            self.package_info_text.insert(tk.END, info)

    def clear_screen(self):
        # Clear all widgets from the screen
        for widget in self.root.winfo_children():
            widget.destroy()

    # Show time frames to see delivery statuses
    def show_time_frames(self):
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(pady=30)

        tk.Label(frame, text="Enter Time Frame (08:00:00 - 13:15:00):").pack(pady=10)

        # Entry for start time
        tk.Label(frame, text="Start Time (HH:MM:SS):").pack(pady=5)
        start_time_entry = tk.Entry(frame)
        start_time_entry.pack(pady=5)

        # Entry for end time
        tk.Label(frame, text="End Time (HH:MM:SS):").pack(pady=5)
        end_time_entry = tk.Entry(frame)
        end_time_entry.pack(pady=5)

        def submit_time_frame():
            start_time_str = start_time_entry.get().strip()
            end_time_str = end_time_entry.get().strip()
            self.display_final_statuses_by_time_frame(start_time_str, end_time_str)

        # Button to submit the time frame
        tk.Button(frame, text="Submit", command=submit_time_frame).pack(pady=10)

        # Add a button to go back to the delivery menu
        tk.Button(frame, text="Back to Delivery Menu", command=self.create_delivery_screen).pack(pady=10)

    # Display final statuses by time frame
    def display_final_statuses_by_time_frame(self, start_time_str, end_time_str):
        # Clear the screen
        self.clear_screen()  
        # Create a frame
        frame = tk.Frame(self.root)
        # Pack the frame
        frame.pack(pady=30)

        # Convert the time strings to time objects
        start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
        end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()

        # Create a label to display the selected time frame
        time_frame_label = tk.Label(frame, text=f"Selected Time Frame: {start_time_str} - {end_time_str}", font=("Helvetica", 14))
        time_frame_label.pack(pady=10)

        # Create a frame to hold the text box and scrollbar
        text_frame = tk.Frame(self.root)
        text_frame.pack(pady=10)

        # Create the text box to display the statuses
        self.log_text = tk.Text(text_frame, height=35, width=160, wrap=tk.NONE)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the scrollbar and attach it to the text box
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Store the original address details of package 9
        original_address = {
            "address": "300 State St",
            "city": "Salt Lake City",
            "zip_code": "84103",
            "weight": 2
        }

        # Sort packages by ID
        sorted_packages = sorted(self.package_status_over_time.items(), key=lambda x: x[0])
        # Display package statuses within the time frame
        for package_id, statuses in sorted_packages:
            package = self.package_setup.get_package_by_id(package_id)
            if not package:
                continue

            # Collect status information within the time frame
            status_info = []  # Store status information
            last_status = None
            last_time = None
            for time, status in statuses:
                status_time = time  # Directly use the time object
                if status_time <= end_time:
                    last_status = status
                    last_time = time
                if start_time <= status_time <= end_time:
                    status_info.append(f"({time.strftime('%H:%M:%S')}: {status})")

            # If no status info in the time frame, use the last known status and time
            if not status_info:
                if last_status and last_time:
                    status_info.append(f"({last_time.strftime('%H:%M:%S')}: {last_status})")
                else:
                    # If no status updates, assume the package is at the hub
                    status_info.append("(Status: At Hub)")

            # Check if package 9 needs to show the updated address
            if package_id == 9:
                if end_time >= datetime.strptime("10:20:00", "%H:%M:%S").time():
                    package.address = "410 S State St"
                    package.city = "Salt Lake City"
                    package.zip_code = "84111"
                    package.weight = 5
                else:
                    package.address = original_address["address"]
                    package.city = original_address["city"]
                    package.zip_code = original_address["zip_code"]
                    package.weight = original_address["weight"]

            # Display the package information
            info = (
                f"Package {package.package_id}: {' | '.join(status_info)}, {package.truck}, {package.address} {package.city}, "
                f"{package.zip_code}, {package.weight}, {package.deadline}\n"
            )
            self.log_text.insert(tk.END, info)

        # Add the "Back to Time Frames" button at the bottom
        tk.Button(self.root, text="Back to Time Frames", command=self.show_time_frames).pack(side=tk.BOTTOM, pady=10)
                
    # Log messages to the UI
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    # Start the delivery process and show packages being delivered in the UI    
    def start_delivery(self, start_time_str=None, end_time_str=None):
        self.log("Delivery started...")
        self.truck1.load_packages_by_id()
        self.truck2.load_packages_by_id()
        self.truck3.load_packages_by_id()

        package_9_has_been_updated = False

        # Start deliveries at 8:00 AM
        base_start_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=8)
        self.start_time = datetime.strptime(start_time_str, "%H:%M:%S") if start_time_str else base_start_time
        self.end_time = datetime.strptime(end_time_str, "%H:%M:%S") if end_time_str else None
        # To handle the packages, store status over time, and combined total distance
        package_handler = self.package_setup  
        self.package_status_over_time = {}
        combined_total_distance = [0]

        # Save the current packages of Truck 3
        current_packages_truck3 = self.truck3.get_all_packages_on_board()

        # Set staggered departure times
        departure_time1 = self.start_time
        departure_time2 = departure_time1 + timedelta(hours=1, minutes=15)
        departure_time3 = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=11, minutes=00)

        # Start delivery routes for each truck
        total_distance1, delivery_route1 = self.graph.start_delivery_route(self.truck1.delivery_nodes, self.truck1.current_location)
        self.truck1.delivery_route = delivery_route1

        total_distance2, delivery_route2 = self.graph.start_delivery_route(self.truck2.delivery_nodes, self.truck2.current_location)
        self.truck2.delivery_route = delivery_route2

        total_distance3, delivery_route3 = self.graph.start_delivery_route(self.truck3.delivery_nodes, self.truck3.current_location)
        self.truck3.delivery_route = delivery_route3

        # Deliver packages for Truck 1
        start_time, _, _, package_9_has_been_updated, delivery_process1, _ = self.truck1.deliver_packages(departure_time1, package_handler, self.package_status_over_time, package_9_has_been_updated, combined_total_distance, current_packages_truck3)
        self.log(f"Truck 1 starting at {start_time.strftime('%H:%M:%S')}")

        # Deliver packages for Truck 2 at 9:15 AM
        start_time2, _, _, package_9_has_been_updated, delivery_process2, _ = self.truck2.deliver_packages(departure_time2, package_handler, self.package_status_over_time, package_9_has_been_updated, combined_total_distance, current_packages_truck3)
        self.log(f"Truck 2 starting at {start_time2.strftime('%H:%M:%S')}")

        # Reassign driver from Truck 1 to Truck 3
        self.driver1.assign_truck(self.truck3)

        # Ensure Truck 3 starts at 11:30 AM
        start_time3, _, _, package_9_has_been_updated, delivery_process3, _ = self.truck3.deliver_packages(departure_time3, package_handler, self.package_status_over_time, package_9_has_been_updated, combined_total_distance, current_packages_truck3)
        self.log(f"Truck 3 starting at {start_time3.strftime('%H:%M:%S')}")

        # Combine delivery processes
        delivery_process = delivery_process1 + delivery_process2 + delivery_process3
        self.log("Delivery Process:\n" + "\n".join(delivery_process))

    # Search for a package by ID
    def search_package_id(self):
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(pady=30)

        # Add label and entry for package ID search
        tk.Label(frame, text="Search by Package ID").pack(pady=10)
        tk.Label(frame, text="Package ID:").pack(pady=5)
        package_id_entry = tk.Entry(frame)
        package_id_entry.pack(pady=5)

        # A function to perform the search
        def perform_search():
            package_id = package_id_entry.get().strip()

            self.log_text.delete(1.0, tk.END)
            # Search for the package by ID
            if package_id:
                package = self.package_setup.get_package_by_id(int(package_id))
                # If the package is found, display the package information
                if package:
                    statuses = self.package_status_over_time.get(int(package_id), [])
                    if statuses:
                        info = (
                            f"ID: {package.package_id}\n"
                            f"Address: {package.address}\n"
                            f"Deadline: {package.deadline}\n"
                            f"City: {package.city}\n"
                            f"Zip Code: {package.zip_code}\n"
                            f"Weight: {package.weight}\n"
                            "Status Timeline:\n"
                        )
                        # Display the status timeline
                        last_status = None
                        for time, status in statuses:
                            if status != last_status:
                                info += f"Time: {time}, Status: {status}, Truck: {package.truck}\n"
                                last_status = status
                        info += "----------------------\n"
                        self.log_text.insert(tk.END, info)
                    else:
                        self.log_text.insert(tk.END, f"No status found for package ID {package_id}\n")
                else:
                    self.log_text.insert(tk.END, f"No package found with ID {package_id}\n")
            else:
                self.log_text.insert(tk.END, "Please enter a Package ID to search.\n")

        # Add search and back buttons
        tk.Button(frame, text="Search", command=perform_search).pack(pady=10)
        tk.Button(frame, text="Back to Delivery Menu", command=self.create_delivery_screen).pack(pady=10)

        # Create a frame to hold the text box and scrollbar
        text_frame = tk.Frame(self.root)
        text_frame.pack(pady=10)

        # Create the text box 
        self.log_text = tk.Text(text_frame, height=20, width=80, wrap=tk.NONE)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the scrollbar and attach it to the text box
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

def main():
    # Create the main window
    root = tk.Tk()
    app = DeliverySystemUI(root)
    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()