from enum import IntEnum


class InstructionType(IntEnum):
    SHORT = 0
    LONG = 1


class ProcessState(IntEnum):
    NEW = 0
    READY = 1
    RUNNING = 2
    BLOCKED = 3
    S_READY = 4
    S_BLOCK = 5
    DEAD = 6


class ExecutionType(IntEnum):
    REGULAR = 0
    CPU_HEAVY = 1
    IO_HEAVY = 2
    MT_GOOD = 3
    MT_BAD = 4
    MT_UGLY = 5
    INS_LONG = 10
    INS_SHORT = 20


class MemoryReferenceType(IntEnum):
    GOOD = 0
    BAD = 1
    UGLY = 2
