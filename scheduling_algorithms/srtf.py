from typing import override
from pcb import PCB
from scheduling_algorithms.scheduling_algorithm import SchedulingAlgorithm


class SRTF(SchedulingAlgorithm):

    @override
    def select_next_process(
        self, ready_queue: list[int], process_table: dict[int, PCB]
    ):
        max_remaining_time_pid = ready_queue[0]
        max_remaining_time = (
            process_table[max_remaining_time_pid].size
            - process_table[max_remaining_time_pid].program_counter
        )

        for i in range(1, len(ready_queue)):
            curr_pid = ready_queue[i]
            curr_remaining_time = (
                process_table[curr_pid].size - process_table[curr_pid].program_counter
            )
            if curr_remaining_time > max_remaining_time:
                max_remaining_time_pid = curr_pid
                max_remaining_time = curr_remaining_time

        return max_remaining_time_pid
