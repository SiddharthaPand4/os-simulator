from simulator_enums import ExecutionType, MemoryReferenceType
from scheduling_algorithms import *
from paging_algorithms import *


config = {
    "processes": {
        "execution_type": {
            ExecutionType.REGULAR: 6,
            ExecutionType.CPU_HEAVY: 2,
            ExecutionType.IO_HEAVY: 2,
        },
        "memory_type": {
            MemoryReferenceType.GOOD: 6,
            MemoryReferenceType.BAD: 3,
            MemoryReferenceType.UGLY: 1,
        },
    },
    "scheduler": {"algorithm": RoundRobin},
    "paging": {"algorithm": SecondChance},
    "mmu_enabled": False,
}
