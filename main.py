"""
Edge Network Compute Node Simulation
-------------------------------------
Entry point. Choose a simulation to run via --sim, or run all three in sequence.

Usage:
    python main.py                 # runs all simulations
    python main.py --sim 1         # single-node, sequential arrival
    python main.py --sim 2         # single-node, burst arrival
    python main.py --sim network   # full 3-node edge network
"""

import argparse

from simulations import test_case_1, test_case_2, network_sim


def main():
    parser = argparse.ArgumentParser(
        description="Edge Network Compute Node Simulation"
    )
    parser.add_argument(
        "--sim",
        choices=["1", "2", "network", "all"],
        default="all",
        help="Simulation to run: 1 | 2 | network | all  (default: all)",
    )
    args = parser.parse_args()

    if args.sim in ("1", "all"):
        test_case_1.run()

    if args.sim in ("2", "all"):
        test_case_2.run()

    if args.sim in ("network", "all"):
        network_sim.run()


if __name__ == "__main__":
    main()
