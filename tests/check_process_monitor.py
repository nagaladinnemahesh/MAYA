from tools.process_monitor import ProcessMonitor


monitor = ProcessMonitor()

print("\nRunning Process Count:")
print(monitor.get_running_process_count())

print("\nTop 5 Memory Consuming Processes:")

for process in monitor.get_top_memory_processes():
    print(
        f"PID: {process['pid']} | "
        f"Name: {process['name']} | "
        f"Memory: {process['memory_mb']} MB"
    )

print("\nTop 5 CPU Consuming Processes:")

for process in monitor.get_top_cpu_processes():
    print(
        f"PID: {process['pid']} | "
        f"Name: {process['name']} | "
        f"CPU: {process['cpu_percent']}%"
    )