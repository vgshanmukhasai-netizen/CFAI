from dataclasses import dataclass
import heapq

# =========================
# CO1: STATE REPRESENTATION
# =========================

@dataclass
class TrafficState:
    north: int
    south: int
    east: int
    west: int

    def total_vehicles(self):
        return self.north + self.south + self.east + self.west


# Simulated sensor readings
current_state = TrafficState(
    north=45,
    south=15,
    east=30,
    west=10
)

print("\n===== CURRENT TRAFFIC STATE =====")
print(current_state)
print("Total Vehicles:", current_state.total_vehicles())


# ==================================
# CO4: UTILITY-BASED DECISION AGENT
# ==================================

def utility_function(vehicle_count):
    return vehicle_count * 2


traffic_dict = {
    "North": current_state.north,
    "South": current_state.south,
    "East": current_state.east,
    "West": current_state.west
}

best_lane = None
highest_utility = -1

print("\n===== UTILITY CALCULATION =====")

for lane, density in traffic_dict.items():
    utility = utility_function(density)
    print(f"{lane}: Utility = {utility}")

    if utility > highest_utility:
        highest_utility = utility
        best_lane = lane

print("\nSelected Lane:", best_lane)


# ==================================
# CO3: CSP-STYLE SIGNAL ALLOCATION
# ==================================

TOTAL_SIGNAL_CYCLE = 120
MIN_GREEN = 15
MAX_GREEN = 60

total_density = sum(traffic_dict.values())

green_times = {}

for lane, density in traffic_dict.items():

    allocated = int(
        (density / total_density)
        * TOTAL_SIGNAL_CYCLE
    )

    allocated = max(MIN_GREEN, allocated)
    allocated = min(MAX_GREEN, allocated)

    green_times[lane] = allocated

print("\n===== SIGNAL ALLOCATION =====")

for lane, time in green_times.items():
    print(f"{lane}: {time} sec")

print(
    f"\nGREEN SIGNAL -> {best_lane} "
    f"for {green_times[best_lane]} sec"
)


# ==================================
# CO2: A* EMERGENCY VEHICLE ROUTING
# ==================================

graph = {
    "Hospital": {
        "J1": 3,
        "J2": 6
    },
    "J1": {
        "J3": 2
    },
    "J2": {
        "J3": 1
    },
    "J3": {
        "AccidentSite": 2
    },
    "AccidentSite": {}
}

heuristic = {
    "Hospital": 5,
    "J1": 3,
    "J2": 2,
    "J3": 1,
    "AccidentSite": 0
}


def astar(start, goal):

    pq = [(0, start)]

    g_cost = {start: 0}

    parent = {}

    while pq:

        _, current = heapq.heappop(pq)

        if current == goal:
            break

        for neighbor, cost in graph[current].items():

            new_cost = g_cost[current] + cost

            if (
                neighbor not in g_cost
                or new_cost < g_cost[neighbor]
            ):

                g_cost[neighbor] = new_cost

                f_cost = (
                    new_cost
                    + heuristic[neighbor]
                )

                heapq.heappush(
                    pq,
                    (f_cost, neighbor)
                )

                parent[neighbor] = current

    path = []
    node = goal

    while node != start:
        path.append(node)
        node = parent[node]

    path.append(start)
    path.reverse()

    return path


# ==================================
# RFID VEHICLE IDENTIFICATION SYSTEM
# ==================================

NORMAL_VEHICLES = {
    "CAR101": "Car",
    "CAR102": "Car",
    "BIKE201": "Bike",
    "BIKE202": "Bike",
    "AUTO301": "Auto Rickshaw",
    "BUS401": "Bus",
    "TRUCK501": "Truck"
}

EMERGENCY_VEHICLES = {
    "AMB001": "Ambulance",
    "AMB002": "Ambulance",

    "POL001": "Police Jeep",
    "POL002": "Police Jeep",

    "FIRE001": "Fire Truck",
    "FIRE002": "Fire Truck"
}

RFID_READ_RANGE = 10  # meters


def detect_vehicle(rfid_tag):

    if rfid_tag in EMERGENCY_VEHICLES:
        return (
            EMERGENCY_VEHICLES[rfid_tag],
            True
        )

    elif rfid_tag in NORMAL_VEHICLES:
        return (
            NORMAL_VEHICLES[rfid_tag],
            False
        )

    else:
        return (
            "Unknown Vehicle",
            False
        )


print("\n===== RFID VEHICLE DETECTION =====")

rfid_tag = input(
    "Scan RFID Tag: "
).strip().upper()

vehicle_distance = float(
    input(
        "Enter vehicle distance from RFID reader (meters): "
    )
)

if vehicle_distance <= RFID_READ_RANGE:

    vehicle_type, emergency_detected = (
        detect_vehicle(rfid_tag)
    )

    print("\nVehicle Type:", vehicle_type)

else:

    print(
        "\nVehicle Out Of RFID Detection Range"
    )

    vehicle_type = "Unknown"
    emergency_detected = False


if emergency_detected:

    print("\n===== EMERGENCY MODE =====")

    emergency_path = astar(
        "Hospital",
        "AccidentSite"
    )

    print(
        f"{vehicle_type} Detected!"
    )

    print(
        "Optimal Route:",
        " -> ".join(emergency_path)
    )

    print(
        "Signal Override Activated."
    )

    print(
        f"Immediate GREEN to {best_lane}"
    )

else:

    print(
        "\nNo Emergency Vehicle Detected."
    )


# ==================================
# FINAL AI DECISION REPORT
# ==================================

print("\n===== AI TRAFFIC CONTROLLER REPORT =====")

print("Traffic Density:", traffic_dict)

print("Selected Lane:", best_lane)

print(
    "Green Duration:",
    green_times[best_lane],
    "seconds"
)

print("Vehicle Type:", vehicle_type)

if emergency_detected:
    print("Emergency Priority: ACTIVE")
else:
    print("Emergency Priority: OFF")

print("System Status: RUNNING")
