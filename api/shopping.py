from fastapi import APIRouter
from fastapi.responses import JSONResponse
import config.settings as conf

router = APIRouter()

@router.get("/api/shopping", tags=["shopping_init"])
async def shopping_init():
    content = {"greeting": "shopping"}
    return JSONResponse(content=content)
