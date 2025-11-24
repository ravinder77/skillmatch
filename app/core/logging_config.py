import logging
import sys


def setup_logging():
    """
    Configure global logging format and level.
    """
    logging.basicConfig(
        level=logging.INFO,  # 👈 change to DEBUG for verbose SQLAlchemy logs
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
