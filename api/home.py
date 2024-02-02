from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import os, sys
sys.path.append(os.pardir)
from db.database import get_db
# from crud.crud import get_all_events


router = APIRouter(
    prefix='/api/home',
    tags=['home']
)

# @router.get("")
# async def home_init(db: Session = Depends(get_db)):
#     events = get_all_events(db=db)
#     if events is None:
#         raise HTTPException(status_code=404, detail="Events not found")
#     print(events[0].event_name)
#     content = {"greeting": "Hello"}
#     return JSONResponse(content=content)

# @router.get("/{id}")
# async def home_init(id: int):
#     content = {"greeting": '{id}'}
#     print(content)
#     return JSONResponse(content=content)
