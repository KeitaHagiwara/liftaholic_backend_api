from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
import os, sys, datetime, time
sys.path.append(os.pardir)
from db.database import get_db
from crud.crud import create_user_if_not_exists

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