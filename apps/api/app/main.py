from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.session import SessionLocal
from app.services.bootstrap import init_db


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    if settings.bootstrap_on_startup:
        with SessionLocal() as db:
            init_db(db=db)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Location Management System API",
        version="0.1.0",
        description="Admin and public API for the Location Management System.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api")
    return app


app = create_app()
