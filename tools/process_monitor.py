import psutil
import time


class ProcessMonitor:

    def get_running_process_count(self):
        return len(psutil.pids())

    def get_running_processes(self):

        processes = []

        for process in psutil.process_iter(
            ["pid", "name", "memory_info"]
        ):
            try:
                info = process.info

                if info["memory_info"] is None:
                    continue

                processes.append({
                    "pid": info["pid"],
                    "name": info["name"],
                    "memory_mb": round(
                        info["memory_info"].rss / (1024 ** 2),
                        2
                    )
                })

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                continue

        return processes

    def get_top_memory_processes(self, limit=5):

        processes = self.get_running_processes()

        processes.sort(
            key=lambda process: process["memory_mb"],
            reverse=True
        )

        return processes[:limit]

    def get_top_cpu_processes(self, limit=5):

        processes = []
        sampled_processes = []

        logical_cores = psutil.cpu_count(logical=True) or 1

        # Initialize CPU measurement
        for process in psutil.process_iter(["pid", "name"]):

            # Exclude System Idle Process
            if process.pid == 0:
                continue

            try:
                process.cpu_percent(interval=None)
                sampled_processes.append(process)

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                continue

        # Wait for CPU sampling
        time.sleep(1)

        # Collect CPU utilization
        for process in sampled_processes:

            try:
                raw_cpu = process.cpu_percent(interval=None)

                # Normalize against total CPU capacity
                normalized_cpu = raw_cpu / logical_cores

                processes.append({
                    "pid": process.pid,
                    "name": process.info["name"],
                    "cpu_percent": round(normalized_cpu, 2)
                })

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                continue

        # Sort by CPU utilization
        processes.sort(
            key=lambda process: process["cpu_percent"],
            reverse=True
        )

        return processes[:limit]