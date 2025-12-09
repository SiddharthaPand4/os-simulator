from frame_entry import FrameEntry
from paging_algorithms.paging_algorithm import PagingAlgorithm
from pcb import PCB


class MMU:

    def __init__(
        self, delta, size, page_size: int, max_pages: int, PagingAlgo: PagingAlgorithm
    ):
        self.time_delta = delta
        self.frame_table: list[FrameEntry] = [None for _ in range(size)]
        self.size = size
        self.page_size = page_size
        self.max_pages = max_pages
        self.paging_algorithm = PagingAlgo()

    def _find_empty_frame_index(self) -> int:
        for frame_no, frame in enumerate(self.frame_table):
            if not frame:
                return frame_no

        return -1

    def handle_page_replacement(self, pcb: PCB, page_no: int, tick: int) -> bool:
        # handle page replacement
        frame_to_clear = self.paging_algorithm.select_frame_to_evict(self.frame_table)
        if frame_to_clear == -1:
            return False
        else:
            # replace the frame with the current page
            self.frame_table[frame_to_clear] = FrameEntry(page_no, pcb.pid, 0, 0, tick)
            pcb.page_table[page_no] = frame_to_clear
            return True

    def load_page_in_memory(self, pcb: PCB, page_no: int, tick: int) -> bool:
        frame_no = self._find_empty_frame_index()
        if frame_no == -1:
            return False
        else:
            frame_entry = FrameEntry(page_no, pcb.pid, 0, 0, tick)
            pcb.page_table[page_no] = frame_no
            self.frame_table[frame_no] = frame_entry
            return True

    def _scan_memory(self, pid: int, page_no: int, tick: int) -> bool:
        for frame in self.frame_table:
            if not frame:
                continue
            if frame.pid == pid and frame.page_no == page_no:
                frame.use = 1
                frame.last_used_tick = tick
                return True
            else:
                if (tick - frame.last_used_tick) > self.time_delta:
                    frame.use = 0

        return False

    def _calculate_pageno(self, memory_reference: int):
        return memory_reference // self.page_size

    def is_page_present(self, pcb: PCB, page_no: int, tick: int) -> bool:
        page_present = self._scan_memory(pcb.pid, page_no, tick)
        return page_present
