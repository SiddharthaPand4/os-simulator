from main_memory_unit import MMU
from pcb import PCB
from process_metrics import ProcessMetrics
from scheduling_algorithms.scheduling_algorithm import SchedulingAlgorithm
from simulator_enums import InstructionType, ProcessState
import os_parameters


class OS:
    def __init__(
        self,
        process_table: dict[int, PCB],
        SchedulingAlgo: SchedulingAlgorithm,
        main_memory_unit: MMU,
        enable_mmu=True,
    ):
        self.mmu_enabled = enable_mmu
        self.main_memory_unit = main_memory_unit
        self.process_table = process_table
        self.ready_queue: list[int] = []
        self.blocked_queue: dict[int, int] = {}  # dict with pid -> rem time of IO
        self.running_pid: int = -1  # no program running at start
        self.scheduling_algorithm = SchedulingAlgo()
        # metrics start
        self.process_metrics: dict[int, ProcessMetrics] = {}
        self.total_ticks = 0
        self.tick = 0
        self.cpu_busy_ticks = 0
        # metrics end

    def initialize_ready_queue(self, process_table: dict[int, PCB]):
        for pid, pcb in process_table.items():
            ready = self.main_memory_unit.load_page_in_memory(pcb, 0, self.tick)
            if ready:
                pcb.state = ProcessState.READY
                self.ready_queue.append(pid)
            else:
                pcb.state = ProcessState.BLOCKED
                self.blocked_queue[pid] = 10

            # metrics start
            self.process_metrics[pid] = ProcessMetrics(pid, pcb.size, arrival_time=0)
            # metrics end

    def handle_block(self, pid: int):
        # called when the process encountered a long sys call
        pcb = self.process_table[pid]
        pcb.state = ProcessState.BLOCKED
        self.blocked_queue[pid] = os_parameters.IO_TIME

    def handle_interrupt(self, pid: int):
        # called when the process time slice ran out
        pcb = self.process_table[pid]
        pcb.state = ProcessState.READY
        self.ready_queue.append(pid)

    def handle_terminate(self, pid: int):
        # called when the process finished
        pcb = self.process_table[pid]
        pcb.state = ProcessState.DEAD
        # metrics start
        self.process_metrics[pid].finish_time = self.tick
        # metrics end

    def handle_page_fault(self, pid: int, page_no: int):
        pcb = self.process_table[pid]
        pcb.state = ProcessState.BLOCKED
        pcb.page_table[page_no] = -1
        # load page
        ready = self.main_memory_unit.load_page_in_memory(pcb, page_no, self.tick)
        if ready:
            pcb.state = ProcessState.READY
            self.ready_queue.append(pid)
        else:
            replaced = self.main_memory_unit.handle_page_replacement(
                pcb, page_no, self.tick
            )
            if replaced:
                pcb.state = ProcessState.BLOCKED
                self.blocked_queue[pid] = os_parameters.PAGE_FAULT_TIME
            else:
                pcb.state = ProcessState.S_BLOCK
                self.blocked_queue[pid] = os_parameters.SUSPEND_TIME

    def execute(self, pcb: PCB):
        # run the instructions of the process
        executed = 0
        while pcb.program_counter < pcb.size and executed < pcb.time_slice:
            instruction = pcb.pointer_to_code[pcb.program_counter]
            # check if the instruction's address is in main memory or not
            if self.mmu_enabled:
                page_no = self.main_memory_unit._calculate_pageno(
                    instruction.address_reference
                )
                if not self.main_memory_unit.is_page_present(pcb, page_no, self.tick):
                    self.handle_page_fault(pcb.pid, page_no)
                    return
            pcb.program_counter += 1
            executed += 1
            self.tick += 1
            # metrics start
            self.cpu_busy_ticks += 1
            self.process_metrics[pcb.pid].total_cpu_time += 1
            # metrics end

            if instruction.syscall == InstructionType.LONG:
                self.handle_block(pcb.pid)
                return

        if pcb.program_counter < pcb.size:
            self.handle_interrupt(pcb.pid)
            return
        else:
            self.handle_terminate(pcb.pid)
            return

    def run(self):
        """does the main job"""
        self.tick = 0
        while len(self.ready_queue) > 0 or len(self.blocked_queue) > 0:
            self.tick += 1

            if self.tick % 10000 == 0:
                print(f"\n---- Tick {self.tick} ----")
                print(f"Running PID {self.running_pid}")
                print(f"READY queue: {self.ready_queue}")
                print(f"BLOCKED queue: {list(self.blocked_queue.keys())}")

            if self.tick > 10e9:
                print("Simulation timeout — possible infinite loop.")
                break

            # decremnt IO waiting time in blocked queue
            self.update_blocked_queue()
            # update the ready queue
            self.update_ready_queue()

            if len(self.ready_queue) == 0:
                continue

            # use the algorithm to pick the next pid
            self.running_pid = self.scheduling_algorithm.select_next_process(
                self.ready_queue, self.process_table
            )

            running_process_pcb = self.process_table[self.running_pid]
            running_process_pcb.state = ProcessState.RUNNING
            # metrics start
            metrics = self.process_metrics[self.running_pid]
            if metrics.start_time is None:
                metrics.start_time = self.tick
                metrics.response_time = self.tick - metrics.arrival_time
            # metrics end
            self.ready_queue.remove(self.running_pid)
            self.execute(running_process_pcb)
            self.running_pid = -1

        self.total_ticks = self.tick

    def update_blocked_queue(self):
        """reduce the waiting time of blocked processes"""
        for pid in self.blocked_queue:
            # decrementing the IO wait time remaining
            self.blocked_queue[pid] = max(0, self.blocked_queue[pid] - 1)

    def update_ready_queue(self):
        # Refresh ready_queue based on PCB states
        io_finished_pids = []
        for pid, rem_time in list(self.blocked_queue.items()):
            if rem_time == 0:
                io_finished_pids.append(pid)

        for pid in io_finished_pids:
            # remove from blocked queue
            self.blocked_queue.pop(pid)
            # add it to the ready queue
            pcb = self.process_table[pid]
            pcb.state = ProcessState.READY
            self.ready_queue.append(pid)

    def shutdown(self):
        if all(pcb.state == ProcessState.DEAD for pcb in self.process_table.values()):
            print("All processes completed. OS is shutting down.")

    def boot(self):
        """starting the OS for the first time"""
        # make the processes in the ready state and store them in the queue
        self.initialize_ready_queue(self.process_table)
        self.run()
        # when run completes
        self.shutdown()

    def report_metrics(self):
        total_tat = total_wt = total_rt = 0
        completed = len(self.process_metrics)
        for pid, metric in self.process_metrics.items():
            t = metric.original_execution_time
            turnaroundtime = metric.finish_time - metric.arrival_time
            waiting_time = turnaroundtime - metric.total_cpu_time
            response_time = metric.response_time
            total_tat += turnaroundtime
            total_wt += waiting_time
            total_rt += response_time
            print(
                f"PID {pid}: T={t} TAT={turnaroundtime}, WT={waiting_time}, RT={response_time}"
            )

        throughput = (completed / self.total_ticks) * 100
        cpu_util = (self.cpu_busy_ticks / self.total_ticks) * 100

        print("\n---- SUMMARY ----")
        print(f"Average TAT: {total_tat/completed:.2f}")
        print(f"Average WT: {total_wt/completed:.2f}")
        print(f"Average RT: {total_rt/completed:.2f}")
        print(f"Throughput: {throughput:.3f} processes/tick")
        print(f"CPU Utilization: {cpu_util:.2f}%")
