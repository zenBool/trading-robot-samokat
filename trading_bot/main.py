from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import router as api_router
from core.config import settings
from core.dependencies import get_broker
from db import db_helper


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # before startup
    broker = get_broker()
    broker.start()

    yield

    # on shutdown
    await db_helper.dispose()  # dispose engine
    broker.stop()
    broker.join()


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.include_router(
    api_router,
    prefix=settings.api.prefix,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
    pass
