from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
import os, sys, datetime, time
from dateutil.relativedelta import relativedelta

sys.path.append(os.pardir)
from db.database import get_db
# select系
from crud.crud import create_user_if_not_exists, crud_get_training_pie_chart, crud_get_total_volume_chart

# ルーターを定義
router = APIRouter(
    prefix='/api/mypage',
    tags=['mypage']
)

# リクエストbodyを定義
class User(BaseModel):
    user_id: str

@router.get("", tags=["mypage_init"])
async def mypage_init():
    content = {"greeting": "Hi!"}
    return JSONResponse(content=content)

# 初回にユーザー作成（サインアップ）した際にDBにアカウント情報を複製する
# usersを新規登録する
@router.post("/create_user", tags=["create_user"])
async def create_user(user:User, db: Session = Depends(get_db)):
    result = None
    try:
        result = create_user_if_not_exists(db=db, user_id=user.user_id)
        statusCode = 200
        statusMessage = "ユーザーを新規登録しました。"
    except Exception as e:
        statusCode = 500
        statusMessage = "ユーザーの新規登録に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "result": result
    }

    return JSONResponse(content=content)

@router.get("/get_user_pie_chart_data/{uid}")
async def get_user_pie_chart_data(uid: str, db: Session = Depends(get_db)):
    result = None
    try:
        today = datetime.datetime.now()
        start_date = datetime.datetime.strftime(today - relativedelta(months=1), '%Y-%m-%d')
        end_date = today.strftime("%Y-%m-%d")
        result = crud_get_training_pie_chart(db=db, user_id=uid, start_date=start_date, end_date=end_date)
        pie_chart_data = []
        for t in result:
            pie_chart_data.append(
                {
                    'value': float(t.pct),
                    'part_no': t.part_no,
                    'part_name': t.part_name,
                    'part_image_file': t.part_image_file
                }
            )
        statusCode = 200
        statusMessage = "ユーザーのトレーニング内訳のデータを取得しました。"

    except Exception as e:
        statusCode = 500
        statusMessage = "ユーザーのトレーニング内訳のデータの取得に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "pie_chart_data": pie_chart_data
    }

    return JSONResponse(content=content)

@router.get("/get_user_total_volume_data/{uid}")
async def get_user_total_volume_data(uid: str, db: Session = Depends(get_db)):
    result = None
    try:
        today = datetime.datetime.now()
        start_date = datetime.datetime.strftime(today - relativedelta(months=1), '%Y-%m-%d')
        end_date = today.strftime("%Y-%m-%d")
        result = crud_get_total_volume_chart(db=db, user_id=uid, start_date=start_date, end_date=end_date)
        training_volume_data = {}
        for t in result:
            key = t.part_no
            if key not in training_volume_data:
                training_volume_data[key] = {
                    'volume_data': [
                        {
                            'volume': float(t.total_volume),
                            'part_name': t.part_name,
                            'datetime': t.datetime
                        }
                    ],
                    'volume_max': float(t.total_volume) * 1.2,
                    'volume_min': float(t.total_volume) * 0.8
                }
            else:
                training_volume_data[key]['volume_data'].append(
                    {
                        'volume': float(t.total_volume),
                        'part_name': t.part_name,
                        'datetime': t.datetime
                    }
                )
                # 最大値と最小値を取得する
                if training_volume_data[key]['volume_max'] < float(t.total_volume):
                    training_volume_data[key]['volume_max'] = float(t.total_volume)
                if training_volume_data[key]['volume_min'] > float(t.total_volume):
                    training_volume_data[key]['volume_min'] = float(t.total_volume)

        statusCode = 200
        statusMessage = "ユーザーのトレーニングボリュームのデータを取得しました。"

    except Exception as e:
        statusCode = 500
        statusMessage = "ユーザーのトレーニングボリュームのデータの取得に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "training_volume_data": training_volume_data,
    }

    return JSONResponse(content=content)