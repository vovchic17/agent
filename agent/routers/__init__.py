from fastapi import APIRouter

from .get_file import router as get_file
from .search import router as search

router = APIRouter()
router.include_router(search)
router.include_router(get_file)
