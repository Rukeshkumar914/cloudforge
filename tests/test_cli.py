import json

import pytest

from app.cli import main

def test_health_command(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["cloudforge", "health"])

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    result = json.loads(captured.out)
    assert result["status"] == "ok"
    assert "operating_system" in result
    assert "python_version" in result

def test_metrics_command(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["cloudforge", "metrics"])

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    result = json.loads(captured.out)
    assert "cpu_percent" in result
    assert "memory_percent" in result
    assert "disk_percent" in result

def test_invalid_command(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["cloudforge", "invalid"])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "invalid choice" in captured.err

def test_missing_command(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["cloudforge"])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "required" in captured.err
