import re
from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(tags=["Поиск"])


DATE_PATTERNS = [
    (
        re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d{3})?)"),
        "%Y-%m-%d %H:%M:%S.%f",
    ),
    (
        re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"),
        "%Y-%m-%d %H:%M:%S",
    ),
    (
        re.compile(r'"timestamp":\s*"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})"'),
        "%Y-%m-%dT%H:%M:%S",
    ),
    (
        re.compile(r"([A-Z][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2})"),
        "%b %d %H:%M:%S",
    ),
]


def extract_datetime(line: str) -> datetime | None:
    """Извлекает datetime из строки лога."""
    for regex, fmt in DATE_PATTERNS:
        match = regex.search(line)
        if match:
            ts = match.group(1)
            try:
                dt = datetime.strptime(ts, fmt)  # noqa: DTZ007
                if "%b %d %H:%M:%S" in fmt:
                    dt = dt.replace(year=datetime.now().year)  # noqa: DTZ005
            except ValueError:
                continue
            else:
                return dt
    return None


class FileMatch(BaseModel):
    """File Match model."""

    filepath: str = Field(description="Имя файла")
    size: int = Field(description="Размер файла в байтах")
    matched_line: str = Field(description="Совпадающая строка")
    line_number: int = Field(description="Номер найденной строки")
    line_datetime: datetime | None = Field(
        default=None,
        description="Дата и время из строки лога",
    )


@router.get("/search")
def search(  # noqa: C901
    root_dir: Annotated[
        str,
        Query(description="Корневая директория для поиска"),
    ],
    query: Annotated[str, Query(description="Поисковый запрос")],
    *,
    recursive: Annotated[
        bool,
        Query(description="Искать рекурсивно"),
    ] = False,
    date_from: Annotated[
        str | None,
        Query(description="Дата начала диапазона (dd.mm.yyyy)"),
    ] = None,
    date_to: Annotated[
        str | None,
        Query(description="Дата конца диапазона (dd.mm.yyyy)"),
    ] = None,
) -> list[FileMatch]:
    def parse_datetime(
        d: str | None,
        *,
        end_of_day: bool = False,
    ) -> datetime | None:
        if d:
            try:
                dt = datetime.strptime(d, "%d.%m.%Y")  # noqa: DTZ007
                if end_of_day:
                    dt = dt.replace(
                        hour=23,
                        minute=59,
                        second=59,
                        microsecond=999999,
                    )
            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid date format: {d}. Use dd.mm.yyyy",
                ) from e
            else:
                return dt
        return None

    df = parse_datetime(date_from)
    dt_ = parse_datetime(date_to, end_of_day=True)

    results: list[FileMatch] = []
    base_path = Path(root_dir)

    if not base_path.is_dir():
        raise HTTPException(
            status_code=400,
            detail=f"'{root_dir}' is not a directory.",
        )

    paths = base_path.rglob("*") if recursive else base_path.iterdir()

    for filepath in paths:
        if filepath.is_file():
            try:
                with filepath.open(encoding="utf-8") as f:
                    for i, line in enumerate(f, start=1):
                        if query not in line:
                            continue

                        line_dt = extract_datetime(line)

                        if line_dt:
                            if df and line_dt < df:
                                continue
                            if dt_ and line_dt > dt_:
                                continue

                        results.append(
                            FileMatch(
                                filepath=str(filepath),
                                size=filepath.stat().st_size,
                                matched_line=line.strip(),
                                line_number=i,
                                line_datetime=line_dt,
                            ),
                        )
            except UnicodeDecodeError:
                continue

    return results
