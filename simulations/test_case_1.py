"""
Test Case 1 — Single node, two processes arriving at different times.

Verifies that the scheduler correctly admits process1 at t=1s, then
admits process2 at t=4s and recalculates both deadlines on the fly.
Snapshots are taken at t=1.5s, 4.5s, 9s, 16s, and 20s.
"""

from src import Compute_node, Process


def run():
    simulation_time = 30  # seconds

    node = Compute_node(
        ipt=20, ram=100, thresh=5,
        time_now=0, simulation_time=simulation_time * 1000,
        name="node-tc1"
    )

    # Nine processes available; only two are used in this test case
    processes = [Process(100, 5, f"process{i}") for i in range(1, 10)]
    p1, p2 = processes[0], processes[1]

    node.add_process(p1, 1 * 1000)
    node.show_stats(1_500)

    node.add_process(p2, 4 * 1000)
    node.show_stats(4_500)
    node.show_stats(9_000)
    node.show_stats(16_000)
    node.show_stats(20_000)

    node.thread.join()

    print(f"\n{'='*60}")
    print(f"  TEST CASE 1 — Single Node, Sequential Process Arrival")
    print(f"{'='*60}")
    for log in node.process_logs:
        print(log)


if __name__ == "__main__":
    run()
