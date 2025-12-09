class FrameEntry:

    def __init__(
        self,
        page_no: int,
        pid: int,
        use: int,
        dirty: int,
        last_used_tick: int,
    ):

        self.page_no = page_no
        self.pid = pid
        self.use = use
        self.dirty = dirty
        self.last_used_tick = last_used_tick
