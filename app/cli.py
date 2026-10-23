import argparse
import json
import logging
import sys
from pathlib import Path

from app.health import get_system_health
from app.monitor import (
    DEFAULT_THRESHOLDS,
    check_thresholds,
    get_system_metrics,
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        prog="cloudforge",
        description="CloudForge - System health and metrics CLI",
    )

    parser.add_argument(
        "command",
        choices=["health", "metrics"],
        help="Command to execute",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Save the report to a JSON file",
    )

    parser.add_argument(
        "--cpu-threshold",
        type=float,
        default=DEFAULT_THRESHOLDS["cpu_percent"],
        help="CPU warning threshold percentage (default: 80)",
    )

    parser.add_argument(
        "--memory-threshold",
        type=float,
        default=DEFAULT_THRESHOLDS["memory_percent"],
        help="Memory warning threshold percentage (default: 80)",
    )

    parser.add_argument(
        "--disk-threshold",
        type=float,
        default=DEFAULT_THRESHOLDS["disk_percent"],
        help="Disk warning threshold percentage (default: 90)",
    )

    args = parser.parse_args()

    logger.info("Executing command: %s", args.command)

    try:
        if args.command == "health":
            result = get_system_health()
        else:
            result = get_system_metrics()

            thresholds = {
                "cpu_percent": args.cpu_threshold,
                "memory_percent": args.memory_threshold,
                "disk_percent": args.disk_threshold,
            }

            warnings = check_thresholds(result, thresholds)

            result["thresholds"] = thresholds
            result["warnings"] = warnings
            result["status"] = "warning" if warnings else "ok"

            if warnings:
                for warning in warnings:
                    logger.warning("%s", warning["message"])
            else:
                logger.info("All system metrics are within thresholds")

        report = json.dumps(result, indent=2)

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report + "\n", encoding="utf-8")
            print(f"Report saved to: {args.output}")
            logger.info("Report exported to %s", args.output)
        else:
            print(report)

        logger.info("Command completed successfully")
        return 0

    except (OSError, ValueError) as exc:
        logger.error("Command failed: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception:
        logger.exception("Unexpected error while executing command")
        print("Error: unexpected internal error. Check application logs.",
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
