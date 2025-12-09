from instruction import Instruction
import os_parameters
from pcb import PCB
from simulator_enums import ExecutionType, InstructionType, MemoryReferenceType
from process import Process
import random


def generate_memory_references(
    min_size: int, max_size: int, process_type: MemoryReferenceType
):
    page_size = os_parameters.PAGE_SIZE
    max_pages = os_parameters.MAX_PAGES
    ref_threshold = max_pages * page_size - 1
    memory_references = []
    # first generate the first 100 or `min_size`` references from the first page
    memory_references.extend(list(range(min_size)))
    # generate next references now
    if process_type == MemoryReferenceType.GOOD:
        consistent_phase_pct = 0.9
    elif process_type == MemoryReferenceType.BAD:
        consistent_phase_pct = 0.5
    else:
        consistent_phase_pct = 0.1

    current_ref = min_size
    consistent_phase = int(consistent_phase_pct * (max_size - min_size))
    for _ in range(consistent_phase):
        # 80% chance to just go to the next line (Sequential) Took Gemini's help for this idea
        if random.random() < 0.8:
            current_ref += 1
        # 20% chance to jump slightly backwards (Small Loop)
        else:
            current_ref -= random.randint(1, 5)
        memory_references.append(min(current_ref, ref_threshold))

    for _ in range(max_size - consistent_phase - min_size):
        memory_references.append(
            min(random.randint(current_ref, ref_threshold), ref_threshold)
        )

    # print(max_size, len(memory_references))
    assert len(memory_references) == max_size

    return memory_references


def create_instructions(
    process_type: ExecutionType, memory_ref_type: MemoryReferenceType
) -> list[Instruction]:
    # create instrcutions accoridng to the type of the process
    threshold = 0.02
    if process_type == ExecutionType.CPU_HEAVY:
        threshold = 0.001
    elif process_type == ExecutionType.IO_HEAVY:
        threshold = 0.2

    min_size = 100
    max_size = os_parameters.MAX_PAGES * os_parameters.PAGE_SIZE
    process_size = max(random.randint(max_size // 2, max_size), min_size)

    # generate memory references
    memory_references = generate_memory_references(min_size, max_size, memory_ref_type)
    instructions = []
    for i in range(process_size):
        instruction_type = (
            InstructionType.SHORT
            if random.random() > threshold
            else InstructionType.LONG
        )
        memory_reference = memory_references[i]
        instructions.append(Instruction(instruction_type, memory_reference))

    return instructions


def create_pcb(
    pid: int,
    uid: int,
    size: int,
    priority: int,
    execution_type: ExecutionType,
    memory_ref_type: MemoryReferenceType,
    pointer_to_code: list[Instruction],
):
    time_slice = random.randint(
        os_parameters.MAX_TIME_SLICE // 2, os_parameters.MAX_TIME_SLICE
    )

    page_table = [-1] * os_parameters.MAX_PAGES

    return PCB(
        pid,
        uid,
        size,
        priority,
        execution_type,
        memory_ref_type,
        pointer_to_code,
        time_slice,
        page_table,
    )


def create_processes(
    process_type_distribution: dict[
        str, dict[ExecutionType | MemoryReferenceType, int]
    ],
    uid=0,
):
    (execution_dist, memory_ref_dist) = process_type_distribution.values()
    execution_types = []
    for execution_type, count in execution_dist.items():
        execution_types.extend([execution_type] * count)

    memory_ref_types = []
    for memory_ref_type, count in memory_ref_dist.items():
        memory_ref_types.extend([memory_ref_type] * count)

    assert (
        len(memory_ref_types) == len(execution_types)
        and len(memory_ref_types) <= os_parameters.MAX_PROCESSESS
    )

    processes = []
    pid = 0
    for execution_type, memory_ref_type in zip(execution_types, memory_ref_types):
        pid += 1
        # create process instructions
        instructions: list[Instruction] = create_instructions(
            execution_type, memory_ref_type
        )
        size = len(instructions)
        priority = random.randint(1, 20)
        # create PCB
        pcb = create_pcb(
            pid,
            uid,
            size,
            priority,
            execution_type,
            memory_ref_type,
            instructions,
        )
        p = Process(pid, uid, instructions, pcb)
        processes.append(p)

    return processes


def create_process_table(processes: list[Process]):
    return {p.id: p.pcb for p in processes}
