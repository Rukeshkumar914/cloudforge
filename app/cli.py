import argparse
import json
import sys

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

    args = parser.parse_args()

    try:
        if args.command == "health":
            result = get_system_health()
        else:
            result = get_system_metrics()

        print(json.dumps(result, indent=2))
        return 0

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
