from fastapi import FastAPI

from src.logger import get_logger
from src.routes import router


logger = get_logger()

logger.log("Starting API", tags=["MAIN"])
app = FastAPI()

app.include_router(router)
