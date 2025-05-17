from fastapi.routing import APIRouter

status_router = APIRouter(prefix="/api", tags=["status"])


@status_router.get("/ping")
def ping():
    return "ok"
