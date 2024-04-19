from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os, sys, datetime, time
sys.path.append(os.pardir)
from db.database import get_db
# select系
from crud.crud import crud_get_all_notifications, crud_get_indiv_notifications, crud_get_unread_notifications_count
# update系
from crud.crud import crud_update_unread_check

router = APIRouter(
    prefix='/api/notification',
    tags=['notification']
)

class UpdateUnreadCheck(BaseModel):
    user_id: str
    notification_id: int


# ----------------------------------------
# ユーザーのお知らせを取得する
# ----------------------------------------
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
                "created_at": datetime.datetime.strftime(notif.created_at, '%Y-%m-%d %H:%M'),
            })
        # あなた向けのお知らせ内容
        for notif in notifications_indiv:
            result_dict['あなた宛'].append({
                "id": notif.id,
                "title": notif.title,
                "detail": notif.detail,
                "type": notif.type,
                "created_at": datetime.datetime.strftime(notif.created_at, '%Y-%m-%d %H:%M'),
            })

        # 未読のお知らせの件数を取得する
        unread_count = crud_get_unread_notifications_count(db=db, user_id=uid)

        statusCode = 200
        statusMessage = "お知らせ情報を取得しました。"

    except Exception as e:

        statusCode = 500
        statusMessage = "お知らせ情報の取得に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "result": result_dict,
        "unreadCount": unread_count
    }
    print(content)
    return JSONResponse(content=content)

# ----------------------------------------
# ユーザーの未読メッセージを既読に変更する
# ----------------------------------------
@router.post("/message_read_check")
async def message_read_check(request: UpdateUnreadCheck, db: Session=Depends(get_db)):
    results = None
    try:
        uid = request.user_id
        crud_update_unread_check(
            db=db,
            user_id=uid,
            notification_id=request.notification_id
        )

        statusCode = 200
        statusMessage = "お知らせメッセージを確認しました。"

    except Exception as e:
        statusCode = 500
        statusMessage = "お知らせメッセージの確認に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "unreadCount": crud_get_unread_notifications_count(db=db, user_id=uid)
    }
    return content
