# Edge Network Compute Node Simulation

A Python-based simulation of an edge computing network with dynamic job scheduling, multi-threaded simulation mechanics, and a custom state-trace logging system. 

## 🚀 Project Overview

This repository demonstrates how to simulate real-time processing and task scheduling in resource-constrained environments like Edge Computing. It models the behavior of multiple devices sharing compute resources, calculating dynamic task execution deadlines on the fly based on current workloads and network transmission overheads.

## 🛠️ Key Features

- **Time-Stepped Simulation:** Leverages Python's `threading` module to advance simulation time in background loops independent of data generation.
- **Dynamic Resource Sharing:** Implements proportional processor sharing. As the active process count goes up or down, CPU allocation (Instructions Per Time unit) is re-divided on the fly.
- **Dynamic Deadline Recalculation:** Accurately recalculates remaining instructions and expected completion times for all running processes when system load changes.
- **Network Latency Modeling:** Includes `Link` and `Sensors` classes to account for physical network limitations, determining delays based on data size, bandwidth, and propagation latency.
- **State-Snapshot Logging System:** Features a targeted logging queue that captures complete snapshots of compute node state and individual process payloads at defined chronological increments.

## 🏗️ Core Architecture

- **`Process` & `Process_compute`:** Defines the task requirements (instruction counts, data size) and captures execution state once admitted to a CPU.
- **`Compute_node`:** The central scheduler and hardware resource abstraction. Manages task admission based on user-defined limits (thresholds) and runs the background execution loop.
- **`Link`:** Dictates the transfer costs of pushing computation payload tasks between devices.
- **`Sensors`:** Randomly distributes generated tasks across available links to model a live edge network.

## 📂 Repository Structure

- `multi_process_node (1) (1).ipynb`: The complete notebook covering the simulator classes, dynamic math, and evaluation test cases.

## 📦 Getting Started

### Prerequisites
To run the simulation, ensure you have Python 3.x and Jupyter installed:
```bash
pip install jupyter
