from pathlib import Path


ROOT = Path(__file__).parent.parent.parent.resolve()
LOG_PATH = ROOT / "logs" / "app.log"
LOG_PATH.parent.mkdir(exist_ok=True)

SETTINGS = {
    "LOG_FILE": LOG_PATH,
    "DEBUG_LOGS": True,
    "LOG_LEVEL": "DEBUG",
    "ALLOWED_TAGS": [
        "CHILE-MAP",    
    ],
}
