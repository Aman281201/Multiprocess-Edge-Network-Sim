import threading

CLOCK_SPEED = 2  # GHz


def get_time(instructions, ipc):
    """Return estimated execution time in milliseconds."""
    duration = (1.0 / CLOCK_SPEED) * (float(instructions) / ipc)
    return round(duration, 2) * 1000


class Process:
    """Incoming job definition: instruction count, data size, and name."""

    def __init__(self, instructions, size, name):
        self.instructions = instructions
        self.size = size
        self.name = name


class Process_compute:
    """
    A Process admitted to a Compute_node.
    Tracks live execution state: instructions remaining, CPU allocation,
    and the projected completion timestamp.
    """

    def __init__(self, process, ipt_alloc, time_now):
        self.process = process
        self.instructions_left = process.instructions
        self.time_started = time_now
        self.last_change_time = time_now
        self.cpu_ipt_allocated = ipt_alloc
        self.time_over = time_now + (self.instructions_left / float(ipt_alloc)) * 1000

    def showData(self):
        return (
            "\n\t\t----------------------------------------------------------------"
            f"\n\t\tProcess Name          : {self.process.name}"
            f"\n\t\tTotal instructions    : {self.process.instructions}"
            f"\n\t\tProcess size          : {self.process.size}"
            f"\n\t\tInstructions left     : {self.instructions_left:.2f}"
            f"\n\t\tTime started          : {self.time_started}"
            f"\n\t\tExpected completion   : {self.time_over:.2f} ms"
            f"\n\t\tLast resource change  : {self.last_change_time}"
            f"\n\t\tCPU IPT allocated     : {self.cpu_ipt_allocated:.2f}"
            "\n\t\t----------------------------------------------------------------"
        )
