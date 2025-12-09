from typing import override
from pcb import PCB
from scheduling_algorithms.scheduling_algorithm import SchedulingAlgorithm


class Priority(SchedulingAlgorithm):

    @override
    def select_next_process(
        self, ready_queue: list[int], process_table: dict[int, PCB]
    ):
        max_priority_pid = ready_queue[0]
        max_priority = process_table[max_priority_pid].priority

        for i in range(1, len(ready_queue)):
            curr_pid = ready_queue[i]
            curr_priority = process_table[curr_pid].priority
            if curr_priority > max_priority:
                max_priority_pid = curr_pid
                max_priority = curr_priority

        return max_priority_pid
