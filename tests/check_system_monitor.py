from tools.system_monitor import SystemMonitor


monitor = SystemMonitor()

print(monitor.get_cpu_usage())
print(monitor.get_memory_usage())
print(monitor.get_battery_status())
print(monitor.get_disk_usage())
print(monitor.get_system_information())