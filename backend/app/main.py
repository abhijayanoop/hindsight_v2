"""App factory: middleware, router mounting, exception handling, health checks."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api.v1.routers import admin, auth, feedback, graph, incidents, recall
from app.config import get_settings
from app.core.logging import configure_logging
from app.db.session import async_session_factory, close_db, init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("starting hindsight backend", extra={"environment": get_settings().environment})
    await init_db()
    yield
    await close_db()
    logger.info("hindsight backend shut down")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "unhandled exception",
            extra={"path": request.url.path, "method": request.method},
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error."},
        )

    @app.get("/health", tags=["meta"])
    async def health() -> dict:
        """Liveness probe: process is up and serving requests."""
        return {"status": "ok"}

    @app.get("/ready", tags=["meta"])
    async def ready() -> JSONResponse:
        """Readiness probe: dependencies (our DB) are reachable."""
        try:
            async with async_session_factory() as session:
                await session.execute(text("SELECT 1"))
        except Exception:
            logger.exception("readiness check failed")
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"status": "not ready", "database": "unreachable"},
            )
        return JSONResponse(content={"status": "ready", "database": "ok"})

    app.include_router(auth.router, prefix=settings.api_v1_prefix)
    app.include_router(incidents.router, prefix=settings.api_v1_prefix)
    app.include_router(recall.router, prefix=settings.api_v1_prefix)
    app.include_router(feedback.router, prefix=settings.api_v1_prefix)
    app.include_router(graph.router, prefix=settings.api_v1_prefix)
    app.include_router(admin.router, prefix=settings.api_v1_prefix)

    return app


app = create_app()
