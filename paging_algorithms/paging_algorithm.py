from abc import ABC, abstractmethod

from main_memory_unit import FrameEntry


class PagingAlgorithm(ABC):

    @abstractmethod
    def select_frame_to_evict(self, frames: list[FrameEntry]) -> int:
        """abstract memthod to override. Selects the frame no on which we should replace the page"""
        pass
