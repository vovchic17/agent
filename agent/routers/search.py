from pathlib import Path
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Query, Request
from pydantic import BaseModel

if TYPE_CHECKING:
    from config_reader import Settings

router = APIRouter(tags=["Поиск"])


class FileMatch(BaseModel):
    """File match model."""

    name: str
    size: int
    matched_line: str


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
                )
                for line in f
                if query in line
            )

    return results
