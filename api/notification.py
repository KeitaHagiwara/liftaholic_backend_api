from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import os, sys, datetime, time
sys.path.append(os.pardir)
from db.database import get_db
from crud.crud import get_all_notifications


router = APIRouter(
    prefix='/api/notification',
    tags=['notification']
)

@router.get("")
async def notification_init(db: Session=Depends(get_db)):
    notifications = get_all_notifications(db=db)
    if notifications is None:
        raise HTTPException(status_code=404, detail="Notifications not found")
    result_list = []
    for notif in notifications:
        print(notif.created_at)
        result_list.append({
            "id": notif.id,
            "title": notif.title,
            "detail": notif.detail,
            "type": notif.type,
            "created_at": datetime.datetime.strftime(notif.created_at, '%Y-%m-%d %H:%M'),
        })
    content = {
        "result": result_list
    }
    content = {"result": result_list}
    return JSONResponse(content=content)