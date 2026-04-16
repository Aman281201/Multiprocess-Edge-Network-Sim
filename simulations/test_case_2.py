"""
Test Case 2 — Single node, burst of seven processes.

Seven processes arrive within the first 5 seconds, flooding up to and beyond
the node's threshold. Tests that the scheduler correctly rate-limits admission,
recalculates CPU shares as processes leave, and produces accurate snapshots
across the full simulation window.
"""

from src import Compute_node, Process


def run():
    simulation_time = 60  # seconds

    node = Compute_node(
        ipt=20, ram=100, thresh=5,
        time_now=0, simulation_time=simulation_time * 1000,
        name="node-tc2"
    )

    processes = [Process(100, 5, f"process{i}") for i in range(1, 10)]
    p1, p2, p3, p4, p5, p6, p7 = processes[:7]

    # First burst: five processes in 2 seconds
    node.add_process(p1, 0.5 * 1000)
    node.add_process(p2, 1.0 * 1000)
    node.add_process(p3, 1.5 * 1000)
    node.add_process(p4, 2.0 * 1000)
    node.add_process(p5, 2.5 * 1000)
    node.show_stats(2_500)

    # Second burst: two more, above threshold
    node.add_process(p6, 4.0 * 1000)
    node.add_process(p7, 5.0 * 1000)

    # Snapshots spread across the full simulation window
    node.show_stats(4_500)
    node.show_stats(5_500)
    node.show_stats(23_000)
    node.show_stats(25_000)
    node.show_stats(30_000)
    node.show_stats(35_000)
    node.show_stats(40_000)

    node.thread.join()

    print(f"\n{'='*60}")
    print(f"  TEST CASE 2 — Single Node, Burst Admission Under Threshold")
    print(f"{'='*60}")
    for log in node.process_logs:
        print(log)


if __name__ == "__main__":
    run()
