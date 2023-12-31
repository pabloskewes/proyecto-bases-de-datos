from pathlib import Path
from project_logger import AppLogger

BASE_DIR = Path(__file__).parent.parent.resolve()
LOG_PATH = BASE_DIR / "logs" / "app.log"
LOG_PATH.parent.mkdir(exist_ok=True)

logger = AppLogger(
    logger_name="backend",
    log_file=LOG_PATH,
    debug_logs=True,
)
logger.allow_tags = [
    # "MAIN",
    # "CRUD",
]
logger.set_level("DEBUG")


def get_logger():
    return logger
