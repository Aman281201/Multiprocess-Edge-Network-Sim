import random

from .process import Process


class Link:
    """
    A directed network link between a Sensor and a Compute_node.

    Models the two physical costs of sending a job:
      - transmission delay  = size / bandwidth
      - propagation delay   = fixed latency of the medium
    """

    def __init__(self, src, dst, bandwidth, prop_delay):
        self.src = src
        self.dst = dst
        self.bandwidth = bandwidth    # bits (or bytes) per time-unit
        self.prop_delay = prop_delay  # fixed latency in ms

    def get_trans_time(self, size):
        return size / self.bandwidth

    def send_msg(self, process, time_now):
        """Forward a process to the destination node, accounting for link delay."""
        arrival = time_now + self.prop_delay + self.get_trans_time(process.size)
        self.dst.add_process(process, arrival)


class Sensors:
    """
    A data-generating edge sensor.

    Holds a list of outgoing Links and, on each send(), picks one at random
    to model non-deterministic routing across the edge network.
    """

    def __init__(self, name):
        self.name = name
        self.links = []
        self._num_sent = 1

    def send(self, time_now, tag="p"):
        """Create a new Process and dispatch it over a randomly chosen link."""
        process = Process(100, 50, f"{self.name}_{self._num_sent}_{tag}")
        link = self.links[random.randint(0, len(self.links) - 1)]
        link.send_msg(process, time_now)
        self._num_sent += 1
