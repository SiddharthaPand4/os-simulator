from typing import override
from pcb import PCB
from scheduling_algorithms.scheduling_algorithm import SchedulingAlgorithm


class SJF(SchedulingAlgorithm):

    @override
    def select_next_process(
        self, ready_queue: list[int], process_table: dict[int, PCB]
    ):
        min_size_pid = ready_queue[0]
        min_size = process_table[min_size_pid].size

        for i in range(1, len(ready_queue)):
            curr_pid = ready_queue[i]
            curr_size = process_table[curr_pid].size
            if curr_size < min_size:
                min_size_pid = curr_pid
                min_size = curr_size

        return min_size_pid
