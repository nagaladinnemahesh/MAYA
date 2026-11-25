import psutil
import platform
import os


class SystemMonitor:

    def get_cpu_usage(self):
        usage = psutil.cpu_percent(interval=1)

        return f"Sir, the current CPU usage is {usage} percent."

    def get_memory_usage(self):
        memory = psutil.virtual_memory()

        total = memory.total / (1024 ** 3)
        available = memory.available / (1024 ** 3)

        return (
            f"Sir, you have {total:.2f} gigabytes of RAM, "
            f"with {available:.2f} gigabytes available. "
            f"Current memory usage is {memory.percent} percent."
        )

    def get_battery_status(self):
        battery = psutil.sensors_battery()

        if battery is None:
            return "Sir, battery information is unavailable."

        status = (
            "connected to power"
            if battery.power_plugged
            else "running on battery"
        )

        return (
            f"Sir, your battery is at {battery.percent} percent "
            f"and the system is {status}."
        )

    def get_disk_usage(self):
        drive = os.environ.get("SystemDrive", "C:") + "\\"

        disk = psutil.disk_usage(drive)

        total = disk.total / (1024 ** 3)
        free = disk.free / (1024 ** 3)

        return (
            f"Sir, your system drive has {total:.2f} gigabytes "
            f"of storage, with {free:.2f} gigabytes free. "
            f"Current disk usage is {disk.percent} percent."
        )

    def get_system_information(self):
        system = platform.system()
        version = platform.release()
        cores = psutil.cpu_count(logical=True)

        return (
            f"Sir, you are running {system} {version}, "
            f"with {cores} logical processors."
        )