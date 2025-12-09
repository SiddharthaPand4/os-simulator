from helpers import create_processes, create_process_table
from main_memory_unit import MMU
from simulator_config import config
from os_sim import OS
import os_parameters


class Simulator:

    def __init__(self):
        # load process_config
        self.config = config
        self.os: OS = None

        process_type_distribution = config["processes"]
        # create processes
        self.processes = create_processes(process_type_distribution)
        print(f"Process Created: {len(self.processes)}")

        # create a scheduler
        process_table = create_process_table(self.processes)
        paging_algorithm = config["paging"]["algorithm"]
        main_memory_unit = MMU(
            os_parameters.TIME_WINDOW_DELTA,
            os_parameters.MAIN_MEMORY_SIZE,
            os_parameters.PAGE_SIZE,
            os_parameters.MAX_PAGES,
            paging_algorithm,
        )
        print(f"MMU Configured with {paging_algorithm} algorithm")
        scheduling_algorithm = config["scheduler"]["algorithm"]
        self.os = OS(
            process_table,
            scheduling_algorithm,
            main_memory_unit,
            enable_mmu=config["mmu_enabled"],
        )
        print(f"Scheduler Configured with {scheduling_algorithm} algorithm")
        print(f"Process Table: \n{process_table}")

    def start(self):
        self.os.boot()
        self.os.report_metrics()


def run():
    simulator = Simulator()
    simulator.start()


if __name__ == "__main__":
    run()
