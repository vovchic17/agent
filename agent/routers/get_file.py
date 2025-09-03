from pathlib import Path as PathLibPath
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import FileResponse

router = APIRouter(tags=["Получение файла"])


@router.get("/file/{filepath}")
def get_log_file(
    filepath: Annotated[
        str,
        Path(
            title="Путь файла",
            description="Путь .log файла для скачивания",
            example="syslog.log",
        ),
    ],
) -> FileResponse:
    log_path = PathLibPath(filepath)

    if (
        not log_path.exists()
        or not log_path.is_file()
        or log_path.suffix != ".log"
    ):
        raise HTTPException(status_code=404, detail="Файл не найден")

    return FileResponse(
        path=log_path,
        filename=log_path.name,
    )
