"""
Network Simulation — 3 edge nodes, 5 sensors, full-mesh links.

Each sensor is connected to every compute node via a Link (bandwidth=10,
prop_delay=1 ms). Every 3 simulation seconds a randomly chosen sensor fires
a task, which travels over a randomly chosen link and is admitted to the
destination node's queue. All three nodes snapshot their state every 500 ms.
Logs are collected and printed in chronological order across all nodes.
"""

import random

from src import Compute_node, Link, Sensors


def run():
    simulation_time = 100  # seconds

    # Edge compute devices
    edge1 = Compute_node(20, 100, 5, 0, simulation_time * 1000, name="edge-1")
    edge2 = Compute_node(20, 100, 5, 0, simulation_time * 1000, name="edge-2")
    edge3 = Compute_node(20, 100, 5, 0, simulation_time * 1000, name="edge-3")
    compute_devices = [edge1, edge2, edge3]

    # Sensors that generate tasks
    sensors = [Sensors(f"s{i}") for i in range(1, 6)]

    # Full-mesh links: every sensor → every compute node
    for sensor in sensors:
        for node in compute_devices:
            sensor.links.append(Link(sensor, node, bandwidth=10, prop_delay=1))

    # Main simulation loop: queue stat snapshots and occasionally fire a sensor
    for t in range(1_000, 50_000, 500):
        for node in compute_devices:
            node.show_stats(t)
        if t % 3_000 == 0:
            random.choice(sensors).send(t)

    # Wait for all background threads to finish
    for node in compute_devices:
        node.thread.join()

    # Interleave logs chronologically across all nodes
    print(f"\n{'='*60}")
    print(f"  NETWORK SIMULATION — 3 edge nodes × 5 sensors")
    print(f"{'='*60}")

    all_logs = [node.process_logs for node in compute_devices]
    max_len = max(len(logs) for logs in all_logs)
    for i in range(max_len):
        for logs in all_logs:
            if i < len(logs):
                print(logs[i])


if __name__ == "__main__":
    run()
