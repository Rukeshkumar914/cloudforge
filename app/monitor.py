import shutil

import psutil


DEFAULT_THRESHOLDS = {
    "cpu_percent": 80.0,
    "memory_percent": 80.0,
    "disk_percent": 90.0,
}


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


def check_thresholds(metrics, thresholds=None):
    """Return warnings for known metrics exceeding their thresholds."""
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    warnings = []

    for metric, limit in thresholds.items():
        if metric not in DEFAULT_THRESHOLDS:
            continue

        if metric not in metrics:
            continue

        value = metrics[metric]

        if value > limit:
            warnings.append({
                "metric": metric,
                "value": value,
                "threshold": limit,
                "message": (
                    f"{metric} is {value}%, "
                    f"above the {limit}% threshold"
                ),
            })

    return warnings


if __name__ == "__main__":
    metrics = get_system_metrics()
    print(metrics)
    print("Warnings:", check_thresholds(metrics))
