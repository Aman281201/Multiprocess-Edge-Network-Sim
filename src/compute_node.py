import threading
import time

from .process import Process_compute


class Compute_node:
    """
    Simulated edge compute device.

    Runs a background thread that advances simulation time in 500 ms steps,
    admitting queued processes up to `thresh`, evicting completed ones, and
    recalculating every running process's CPU share and deadline on each tick.
    """

    def __init__(self, ipt, ram, thresh, time_now, simulation_time, name="compute_node"):
        self.name = name
        self.IPT = ipt          # total Instructions Per Time-unit for this node
        self.RAM = ram
        self.thresh = thresh    # max concurrent processes
        self.num_process = 0

        self.processes = []     # list of Process_compute currently running
        self.message_queue = [] # list of (arrival_time, Process) waiting to be admitted
        self.show_queue = []    # list of simulation timestamps at which to snapshot state
        self.process_logs = []  # accumulated log strings produced by show()

        self.time_created = time_now
        self.simulation_time = simulation_time

        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    # ------------------------------------------------------------------
    # Background simulation loop
    # ------------------------------------------------------------------

    def _run(self):
        """Advance simulation time in 500 ms steps until simulation_time is reached."""
        time_now = 0
        time.sleep(0.3)  # small startup delay so the caller can finish setup
        while time_now < self.time_created + self.simulation_time:
            time_now += 500
            self.update_processes(time_now)

    # ------------------------------------------------------------------
    # Scheduling core
    # ------------------------------------------------------------------

    def update_processes(self, time_now):
        # 1. Remove completed processes
        remove_list = [p for p in self.processes if p.time_over < time_now]
        for p in remove_list:
            self.processes.remove(p)

        # 2. Admit queued processes if below threshold
        add_list = []
        if self.num_process < self.thresh or len(remove_list) > 0:
            while (
                self.num_process <= self.thresh
                and self.message_queue
                and (self.num_process + len(add_list) - len(remove_list) < self.thresh)
            ):
                if self.message_queue[0][0] <= time_now:
                    add_list.append(self.message_queue[0][1])
                    self.message_queue.pop(0)
                else:
                    break

        # 3. Recalculate counts
        self.num_process = self.num_process + len(add_list) - len(remove_list)

        # 4. Re-divide CPU share and reproject deadlines for running processes
        for p in self.processes:
            p.instructions_left -= p.cpu_ipt_allocated * (float(time_now - p.last_change_time) / 1000)
            if self.num_process > 0:
                p.cpu_ipt_allocated = float(self.IPT) / self.num_process
            timedelta_s = p.instructions_left / float(p.cpu_ipt_allocated)
            p.time_over = time_now + timedelta_s * 1000
            p.last_change_time = time_now

        # 5. Admit new processes with their fair share
        for proc in add_list:
            alloc = float(self.IPT) / self.num_process if self.num_process > 0 else float(self.IPT)
            self.processes.append(Process_compute(proc, alloc, time_now))

        # 6. Emit a log snapshot if one is due
        if self.show_queue and self.show_queue[0] <= time_now:
            self.show_queue.pop(0)
            self._snapshot(time_now)

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def _snapshot(self, time_now):
        """Capture a full state snapshot into process_logs."""
        log = (
            f"\n\t============================================================"
            f"\n\tCompute node : {self.name}"
            f"\n\tSimulation t : {time_now} ms"
            f"\n\tProcesses    : {self.num_process} running"
            f"\n\t------------------------------------------------------------"
        )
        for p in self.processes:
            log += p.showData()
        log += "\n\t============================================================\n"
        self.process_logs.append(log)

    def show_stats(self, time_ms):
        """Queue a state snapshot to be emitted when simulation time reaches time_ms."""
        self.show_queue.append(time_ms)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def add_process(self, process, arrival_time_ms):
        """Schedule a process to be admitted at arrival_time_ms."""
        self.message_queue.append((arrival_time_ms, process))

    def when_free(self, time_now):
        """Return the earliest time this node will drop below its threshold."""
        self.update_processes(time_now)
        if self.num_process < self.thresh:
            return time_now - 100  # already free
        return min(p.time_over for p in self.processes)
