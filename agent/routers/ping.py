from fastapi import APIRouter

router = APIRouter(tags=["Проверка подключения"])


@router.get("/ping")
def ping() -> str:
    return "pong"
