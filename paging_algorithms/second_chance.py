from typing import override
from main_memory_unit import FrameEntry
from paging_algorithms.paging_algorithm import PagingAlgorithm


class SecondChance(PagingAlgorithm):

    @override
    def select_frame_to_evict(self, frames: list[FrameEntry]) -> int:
        eligible_frames = [
            (i, frame) for i, frame in enumerate(frames) if frame is not None
        ]
        if len(eligible_frames) == 0:
            return -1

        for frame_no, frame in eligible_frames[1:]:
            if frame.use == 0:
                return frame_no

        return -1
