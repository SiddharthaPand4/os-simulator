from pcb import PCB


class ProcessTable:
    def __init__(self, table: dict[int, PCB]):
        self.table = table  # pid -> PCB
