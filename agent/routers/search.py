from pathlib import Path
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Query, Request
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from config_reader import Settings

router = APIRouter(tags=["Поиск"])


class FileMatch(BaseModel):
    """File match model."""

    name: str = Field(description="Имя файла")
    size: int = Field(description="Размер файла в байтах")
    matched_line: str = Field(description="Совпадающая строка")
    line_number: int = Field(description="Номер найденной строки")


@router.get("/search")
def search(
    request: Request,
    query: Annotated[str, Query(description="Поисковый запрос")],
) -> list[FileMatch]:
    config: Settings = request.app.state.config
    results: list[FileMatch] = []

    for filename in Path.iterdir(config.LOG_DIR):
        filepath = Path(config.LOG_DIR) / filename
        with filepath.open(encoding="utf-8") as f:
            results.extend(
                FileMatch(
                    name=filename.name,
                    size=filepath.stat().st_size,
                    matched_line=line.strip(),
                    line_number=i,
                )
                for i, line in enumerate(f, start=1)
                if query in line
            )

    return results
