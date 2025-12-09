class PageTableEntry:

    def __init__(self, page_no: int, frame_no: int, pid: int):
        self.page_no = page_no
        self.frame_no = frame_no
        self.pid = pid


class PageTable:

    def __init__(self, page_table_entries: list[PageTableEntry]):
        self.entries = page_table_entries
