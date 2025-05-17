import json
import logging
import os
import sys

from fastapi import Request
from fastapi.applications import FastAPI
from loguru import logger
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import _StreamingResponse
from starlette.middleware.cors import CORSMiddleware

from .api.ping import status_router
from .api.v1.auth.views import auth_router
from .external.postgres.connection import (
    connect_postgres,
    disconnect_postgres,
    init_database,
)
from .settings import settings

if settings.debug_mode:
    docs_url = "/api/docs"
    redoc_url = "/api/redoc"
else:
    docs_url = None
    redoc_url = None


app = FastAPI(
    title="Auth backend",
    docs_url=docs_url,
    redoc_url=redoc_url,
    version=os.getenv("APP_VERSION", default="DEV"),
)


logger_config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<level>{level}: {message}</level>",  # noqa
        }
    ]
}


def create_app():
    app.include_router(status_router)
    app.include_router(auth_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", connect_postgres)
    app.add_event_handler("startup", init_database)
    app.add_event_handler("shutdown", disconnect_postgres)

    return app
