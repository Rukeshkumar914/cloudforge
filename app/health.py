import platform
import shutil


def get_system_health():
    disk = shutil.disk_usage("/")

    return {
        "status": "ok",
        "operating_system": platform.system(),
        "python_version": platform.python_version(),
        "disk_total_gb": round(disk.total / (1024 ** 3), 2),
        "disk_free_gb": round(disk.free / (1024 ** 3), 2),
    }


if __name__ == "__main__":
    print(get_system_health())
