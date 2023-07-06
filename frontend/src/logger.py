from pathlib import Path
from project_logger import AppLogger

BASE_DIR = Path(__file__).parent.parent.resolve()
LOG_PATH = BASE_DIR / "logs" / "app.log"
LOG_PATH.parent.mkdir(exist_ok=True)

logger = AppLogger(
    logger_name="frontend",
    log_file=LOG_PATH,
    debug_logs=True,
)
logger.allow_tags = [
    # "CHILE-MAP",
    # "BUSCADOR-RECORRIDOS",
    "TABLA-RECORRIDOS",
]
logger.set_level("DEBUG")
logger.log(f"Logger initialized using tags {logger.allow_tags}")


def get_logger():
    return logger
