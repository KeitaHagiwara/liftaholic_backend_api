from fastapi import APIRouter
from fastapi.responses import JSONResponse
import config.settings as conf

router = APIRouter()

@router.get("/api/workout", tags=["workout_init"])
async def workout_init():
    content = {"greeting": "workout"}
    return JSONResponse(content=content)
