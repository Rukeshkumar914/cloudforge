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
    assert "warnings" in result
    assert result["status"] in ["ok", "warning"]


def test_health_report_export(monkeypatch, capsys, tmp_path):
    output_file = tmp_path / "reports" / "health.json"
    monkeypatch.setattr(
        "sys.argv",
        ["cloudforge", "health", "--output", str(output_file)],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert output_file.exists()
    assert "Report saved to:" in captured.out

    result = json.loads(output_file.read_text(encoding="utf-8"))
    assert result["status"] == "ok"
    assert "operating_system" in result


def test_metrics_report_export(monkeypatch, capsys, tmp_path):
    output_file = tmp_path / "metrics.json"
    monkeypatch.setattr(
        "sys.argv",
        ["cloudforge", "metrics", "--output", str(output_file)],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert output_file.exists()
    assert "Report saved to:" in captured.out

    result = json.loads(output_file.read_text(encoding="utf-8"))
    assert "cpu_percent" in result
    assert "memory_percent" in result
    assert "disk_percent" in result
    assert "warnings" in result


def test_report_export_os_error(monkeypatch, capsys, tmp_path):
    output_file = tmp_path / "health.json"

    monkeypatch.setattr("sys.argv", [
        "cloudforge", "health", "--output", str(output_file)
    ])

    def fail_write(*args, **kwargs):
        raise OSError("Permission denied")

    monkeypatch.setattr("pathlib.Path.write_text", fail_write)

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error: Permission denied" in captured.err


def test_unexpected_error_is_handled(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["cloudforge", "health"])

    def fail_health():
        raise RuntimeError("simulated failure")

    monkeypatch.setattr("app.cli.get_system_health", fail_health)

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "unexpected internal error" in captured.err


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
