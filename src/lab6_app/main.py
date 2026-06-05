from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse

from src.lab6_app.exceptions import (
    MetricAlreadyExistsError,
    MetricNotFoundError,
    TerritoryNotFoundError,
)
from src.lab6_app.init_dependencies import init_dependencies
from src.lab6_app.routes.analysis import router as analysis_router
from src.lab6_app.routes.config import router as config_router
from src.lab6_app.routes.territories import router as territories_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    deps = init_dependencies()
    app.state.dependencies = deps
    logger.info("Application dependencies initialized")
    yield
    logger.info("Application shutdown")


app = FastAPI(
    lifespan=lifespan,
    title="Laboratory FastAPI App",
    description="Учебное приложение на FastAPI",
    version="1.0.0",
)


@app.exception_handler(TerritoryNotFoundError)
async def territory_not_found_handler(request: Request, exc: TerritoryNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(MetricNotFoundError)
async def metric_not_found_handler(request: Request, exc: MetricNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(MetricAlreadyExistsError)
async def metric_already_exists_handler(request: Request, exc: MetricAlreadyExistsError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.get("/")
async def get_root():
    return RedirectResponse("/docs")


@app.get("/ping")
async def ping_server():
    return "pong"


app.include_router(config_router)
app.include_router(analysis_router)
app.include_router(territories_router)
