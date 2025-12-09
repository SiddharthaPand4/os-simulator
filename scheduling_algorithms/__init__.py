from .fcfs import FCFS
from .sjf import SJF
from .rr import RoundRobin
from .priority import Priority
from .srtf import SRTF
from .ljf import LJF

# Optional: define what gets imported with *
__all__ = ["FCFS", "SJF", "RoundRobin", "Priority", "SRTF", "LJF"]
