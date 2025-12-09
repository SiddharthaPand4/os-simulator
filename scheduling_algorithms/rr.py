from typing import override
from pcb import PCB
from scheduling_algorithms.scheduling_algorithm import SchedulingAlgorithm


class RoundRobin(SchedulingAlgorithm):

    @override
    def select_next_process(
        self, ready_queue: list[int], process_table: dict[int, PCB]
    ):
        return ready_queue[0]
