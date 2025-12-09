from typing import override
from main_memory_unit import FrameEntry
from paging_algorithms.paging_algorithm import PagingAlgorithm


class LRU(PagingAlgorithm):

    @override
    def select_frame_to_evict(self, frames: list[FrameEntry]) -> int:
        eligible_frames = [
            (i, frame.last_used_tick)
            for i, frame in enumerate(frames)
            if frame is not None
        ]
        if len(eligible_frames) == 0:
            return -1

        oldest_frame_no, oldest_use_tick = eligible_frames[0]
        for frame_no, last_used_tick in eligible_frames[1:]:
            if last_used_tick < oldest_use_tick:
                oldest_frame_no, oldest_use_tick = frame_no, last_used_tick

        return oldest_frame_no
