from app.monitor import get_system_metrics


def test_system_metrics():
    metrics = get_system_metrics()

    assert 0 <= metrics["cpu_percent"] <= 100
    assert 0 <= metrics["memory_percent"] <= 100
    assert 0 <= metrics["disk_percent"] <= 100
    assert metrics["memory_available_mb"] >= 0
    assert metrics["disk_free_gb"] >= 0
