from app.health import get_system_health


def test_system_health():
    result = get_system_health()

    assert result["status"] == "ok"
    assert result["operating_system"] == "Linux"
    assert result["disk_total_gb"] > 0
    assert result["disk_free_gb"] >= 0
