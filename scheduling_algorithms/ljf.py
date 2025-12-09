from typing import override
from pcb import PCB
from scheduling_algorithms.scheduling_algorithm import SchedulingAlgorithm


class LJF(SchedulingAlgorithm):

    @override
    def select_next_process(
        self, ready_queue: list[int], process_table: dict[int, PCB]
    ):
        max_size_pid = ready_queue[0]
        max_size = process_table[max_size_pid].size

        for i in range(1, len(ready_queue)):
            curr_pid = ready_queue[i]
            curr_size = process_table[curr_pid].size
            if curr_size > max_size:
                max_size_pid = curr_pid
                max_size = curr_size

        return max_size_pid
