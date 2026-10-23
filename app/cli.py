
import argparse
import json
import sys
from pathlib import Path

from app.health import get_system_health
from app.monitor import get_system_metrics


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

    args = parser.parse_args()

    try:
        if args.command == "health":
            result = get_system_health()
        else:
            result = get_system_metrics()

        report = json.dumps(result, indent=2)

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report + "\n", encoding="utf-8")
            print(f"Report saved to: {args.output}")
        else:
            print(report)

        return 0

    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

