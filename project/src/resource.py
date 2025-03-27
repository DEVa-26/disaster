import numpy as np
import threading
import time
from scipy.optimize import linprog

# Define disaster types and severity levels
disaster_types = ["Earthquake", "Flood", "Hurricane", "Fire", "Landslide"]
severity_levels = ["Little to None", "Mild", "Severe"]

# Resource types and their max availability (global resources)
resources = {
    "ambulance": 200,
    "fire truck": 80,
    "helicopter rescue": 10,
    "earth movers": 120,
    "search and rescue": 350,
    "first aid teams": 250,
    "rescue boats": 40
}

# Scaled priority allocation matrix (scaling up improves numerical stability)
allocation_matrix = np.array([
    [60,   0,  50, 80, 80,  80,  0],   # Earthquake
    [10,    0, 80,   0, 80, 50,80],   # Flood
    [50,    0, 50,   40, 80, 80, 50],   # Hurricane
    [70,  80,   20,   0,  50, 80,  0],   # Fire
    [50,    0,  30, 80,  70,  70,  0]    # Landslide
])

# Convert severity level to a scaling factor
severity_scale = {
    "Little to None": 0.2,
    "Mild": 0.5,
    "Severe": 1.0
}

# Dictionary to store timers for each resource
resource_timers = {}
0
# Function to restore resources after timer ends
def restore_resources(allocated_resources):
    time.sleep(30)  # Simulate resource usage time (30 seconds)
    for resource, amount in allocated_resources.items():
        resources[resource] += amount  # Restore the allocated resources
    print("\n✅ Resources restored after usage!\n")

def allocate_resources(disaster_type, severity_level):
    if disaster_type not in disaster_types:
        print("Invalid disaster type!")
        return
    if severity_level not in severity_scale:
        print("Invalid severity level!")
        return

    global resources  # Ensure we modify the global resource dictionary

    # Scale the disaster's priority row by the severity factor
    severity_factor = severity_scale[severity_level]
    scaled_priority = allocation_matrix[disaster_types.index(disaster_type)] * severity_factor

    # Objective: maximize sum( scaled_priority[j] * x[j] )
    c = -scaled_priority

    # Each resource x[j] is bounded between 0 and available resources (ensuring at least 20% remains)
    bounds = [(0, 0.8 * resources[res]) for res in resources.keys()]

    # Solve the linear program
    result = linprog(c, bounds=bounds, method="highs-ds")
    
    if result.success:
        allocated_resources = result.x
        allocated_dict = {}  # Store allocated resources

        print(f"\n🚨 Optimized Resource Allocation for {disaster_type} ({severity_level} severity):")
        for i, resource in enumerate(resources.keys()):
            allocated = int(round(allocated_resources[i]))
            resources[resource] -= allocated  # Reduce the available resources
            allocated_dict[resource] = allocated  # Store allocation for restoration
            print(f"  - {resource}: {allocated} (Remaining: {resources[resource]})")
        
        # Start a background thread to restore resources after a delay
        restore_thread = threading.Thread(target=restore_resources, args=(allocated_dict,))
        restore_thread.start()
    
    else:
        print("Optimization Failed!")

# Example usage:
allocate_resources("Flood", "Severe")
allocate_resources("Earthquake", "Mild")  # Next allocation will use updated resources
time.sleep(60)
allocate_resources("Flood", "Mild")
