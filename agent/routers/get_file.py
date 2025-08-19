from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, HTTPException, Path, Request
from fastapi.responses import FileResponse

if TYPE_CHECKING:
    from config_reader import Settings


router = APIRouter(tags=["Получение файла"])


@router.get("/file/{filename}")
def get_log_file(
    request: Request,
    filename: Annotated[
        str,
        Path(
            title="Имя файла",
            description="Имя .log файла для скачивания",
            example="syslog.log",
        ),
    ],
) -> FileResponse:
    config: Settings = request.app.state.config
    log_path = config.LOG_DIR / filename
    if (
        not log_path.exists()
        or not log_path.is_file()
        or log_path.suffix != ".log"
    ):
        raise HTTPException(status_code=404, detail="Файл не найден")

    return FileResponse(
        path=log_path,
        filename=filename,
    )
