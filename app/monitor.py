
import shutil

import psutil


def get_system_metrics():
    memory = psutil.virtual_memory()
    disk = shutil.disk_usage("/")

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": memory.percent,
        "memory_available_mb": round(
            memory.available / (1024 ** 2), 2
        ),
        "disk_percent": round(
            disk.used / disk.total * 100, 2
        ),
        "disk_free_gb": round(
            disk.free / (1024 ** 3), 2
        ),
    }


if __name__ == "__main__":
    print(get_system_metrics())
