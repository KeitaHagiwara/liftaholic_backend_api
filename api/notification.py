from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import os, sys, datetime, time
sys.path.append(os.pardir)
from db.database import get_db
from crud.crud import crud_get_all_notifications, crud_get_indiv_notifications


router = APIRouter(
    prefix='/api/notification',
    tags=['notification']
)

@router.get("/{uid}")
async def notification_init(uid: str, db: Session=Depends(get_db)):
    result_dict = {}
    try:
        notifications = crud_get_all_notifications(db=db)
        notifications_indiv = crud_get_indiv_notifications(db=db, user_id=uid)

        if notifications is None or notifications_indiv is None:
            raise HTTPException(status_code=404, detail="Notifications not found")

        result_dict = {'ニュース': [], 'あなた宛': []}
        # 全体向けのお知らせ内容
        for notif in notifications:
            result_dict['ニュース'].append({
                "id": notif.id,
                "title": notif.title,
                "detail": notif.detail,
                "type": notif.type,
                "animation_link": notif.animation_link,
                "animation_width": notif.animation_width,
                "created_at": datetime.datetime.strftime(notif.created_at, '%Y-%m-%d %H:%M'),
            })
        # あなた向けのお知らせ内容
        for notif in notifications_indiv:
            result_dict['あなた宛'].append({
                "id": notif.id,
                "title": notif.title,
                "detail": notif.detail,
                "type": notif.type,
                "animation_link": notif.animation_link,
                "animation_width": notif.animation_width,
                "created_at": datetime.datetime.strftime(notif.created_at, '%Y-%m-%d %H:%M'),
            })

        statusCode = 200
        statusMessage = "お知らせ情報を取得しました。"

    except Exception as e:

        statusCode = 500
        statusMessage = "お知らせ情報の取得に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "result": result_dict
    }
    return JSONResponse(content=content)