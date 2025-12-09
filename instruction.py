from simulator_enums import InstructionType


class Instruction:
    def __init__(self, syscall: InstructionType, address_reference=None):
        self.syscall = syscall  # 0 (short) or 1 (long)
        self.address_reference = address_reference
