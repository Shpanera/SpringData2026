from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse


from src.lab6_app.routes.analysis import router as analysis_router
from src.lab6_app.routes.config import router as config_router
from src.lab6_app.init_dependencies import init_dependencies

from src.lab6_app.routes.territories import router as territories_router




@asynccontextmanager
async def lifespan(app: FastAPI):
    deps = init_dependencies()
    app.state.dependencies = deps
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Laboratory FastAPI App",
    description="Учебное приложение на FastAPI",
    version="1.0.0",
)


@app.get("/")
async def get_root():
    return RedirectResponse("/docs")


@app.get("/ping")
async def ping_server():
    return "pong"


app.include_router(config_router)
app.include_router(analysis_router)
app.include_router(territories_router)
