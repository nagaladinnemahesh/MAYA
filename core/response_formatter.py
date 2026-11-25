class ResponseFormatter:

    def format_process_count(self, count):
        return (
            f"Sir, there are currently "
            f"{count} running processes."
        )

    def format_memory_processes(self, processes):

        if not processes:
            return "Sir, no process memory data is available."

        response = (
            f"Sir, here are the top {len(processes)} "
            "memory-consuming processes. "
        )

        for index, process in enumerate(processes, start=1):

            response += (
                f"Number {index}, "
                f"{process['name']}, "
                f"using {process['memory_mb']:.1f} "
                "megabytes of memory. "
            )

        return response

    def format_cpu_processes(self, processes):

        if not processes:
            return "Sir, no process CPU data is available."

        response = (
            f"Sir, here are the top {len(processes)} "
            "CPU-consuming processes. "
        )

        for index, process in enumerate(processes, start=1):

            response += (
                f"Number {index}, "
                f"{process['name']}, "
                f"using {process['cpu_percent']:.2f} "
                "percent of total CPU capacity. "
            )

        return response