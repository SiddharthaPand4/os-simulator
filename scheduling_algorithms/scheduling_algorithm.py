from abc import ABC, abstractmethod

from pcb import PCB


class SchedulingAlgorithm(ABC):

    @abstractmethod
    def select_next_process(
        self, ready_queue: list[int], process_table: dict[int, PCB]
    ):
        """abstract memthod to override"""
        pass
