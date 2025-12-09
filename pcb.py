from instruction import Instruction
from simulator_enums import ProcessState, ExecutionType, MemoryReferenceType


class PCB:
    def __init__(
        self,
        pid: int,
        uid: int,
        size: int,
        priority: int,
        execution_type: ExecutionType,
        memory_reference_type: MemoryReferenceType,
        pointer_to_code: list[Instruction],
        time_slice,
        page_table: list[int],
    ):
        self.pid = pid
        self.uid = uid
        self.size = size
        self.priority = priority
        self.state = ProcessState.NEW  # READY, RUNNING, BLOCKED, etc.
        self.program_counter = 0
        self.process_type = execution_type
        self.page_table = page_table
        self.time_slice = time_slice
        self.memory_behavior = memory_reference_type
        self.pointer_to_code = pointer_to_code
