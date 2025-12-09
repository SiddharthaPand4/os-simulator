from instruction import Instruction
from pcb import PCB


class Process:
    def __init__(self, pid: int, uid: int, instructions: list[Instruction], pcb: PCB):
        self.id = pid
        self.owner_id = uid
        self.instructions = instructions
        self.pcb = pcb
        self.size = len(instructions)
