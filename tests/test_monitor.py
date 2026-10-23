from app.monitor import (
    DEFAULT_THRESHOLDS,
    check_thresholds,
    get_system_metrics,
)


def test_system_metrics():
    metrics = get_system_metrics()

    assert "cpu_percent" in metrics
    assert "memory_percent" in metrics
    assert "memory_available_mb" in metrics
    assert "disk_percent" in metrics
    assert "disk_free_gb" in metrics


def test_default_thresholds():
    assert DEFAULT_THRESHOLDS == {
        "cpu_percent": 80.0,
        "memory_percent": 80.0,
        "disk_percent": 90.0,
    }


def test_no_threshold_warnings():
    metrics = {
        "cpu_percent": 20.0,
        "memory_percent": 40.0,
        "disk_percent": 50.0,
    }

    assert check_thresholds(metrics) == []


def test_cpu_threshold_warning():
    metrics = {
        "cpu_percent": 95.0,
        "memory_percent": 40.0,
        "disk_percent": 50.0,
    }

    warnings = check_thresholds(metrics)

    assert len(warnings) == 1
    assert warnings[0]["metric"] == "cpu_percent"
    assert warnings[0]["value"] == 95.0
    assert warnings[0]["threshold"] == 80.0


def test_multiple_threshold_warnings():
    metrics = {
        "cpu_percent": 95.0,
        "memory_percent": 90.0,
        "disk_percent": 96.0,
    }

    warnings = check_thresholds(metrics)

    assert len(warnings) == 3


def test_custom_thresholds():
    metrics = {
        "cpu_percent": 75.0,
        "memory_percent": 60.0,
        "disk_percent": 50.0,
    }

    thresholds = {
        "cpu_percent": 70.0,
        "memory_percent": 80.0,
        "disk_percent": 90.0,
    }

    warnings = check_thresholds(metrics, thresholds)

    assert len(warnings) == 1
    assert warnings[0]["metric"] == "cpu_percent"


def test_equal_to_threshold_is_not_warning():
    metrics = {
        "cpu_percent": 80.0,
        "memory_percent": 80.0,
        "disk_percent": 90.0,
    }

    assert check_thresholds(metrics) == []


def test_unknown_metric_is_skipped():
    metrics = {
        "cpu_percent": 20.0,
        "custom_metric": 99.0,
    }

    thresholds = {
        "cpu_percent": 80.0,
        "custom_metric": 50.0,
    }

    warnings = check_thresholds(metrics, thresholds)

    assert warnings == []
