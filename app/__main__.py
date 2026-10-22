import logging
import sys

from app.cli import main


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stderr,
)

if __name__ == "__main__":
    raise SystemExit(main())
