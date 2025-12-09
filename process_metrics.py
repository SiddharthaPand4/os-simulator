class ProcessMetrics:

    def __init__(self, pid: int, execution_time, arrival_time: int = 0):
        self.pid = pid
        self.original_execution_time = execution_time
        self.arrival_time = arrival_time
        self.start_time = None
        self.finish_time = None
        self.total_cpu_time = 0
        self.waiting_time = 0  # (optional — can compute later)
        self.response_time = None  # computed once at start
