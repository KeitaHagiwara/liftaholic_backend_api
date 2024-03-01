from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import os, sys, datetime, time
sys.path.append(os.pardir)
from db.database import get_db
from crud.crud import crud_get_user_training_menu


router = APIRouter(
    prefix='/api/workout',
    tags=['workout']
)

@router.get("/api/workout", tags=["workout_init"])
async def workout_init():
    content = {"greeting": "workout"}
    return JSONResponse(content=content)

@router.get("/get_user_training_menu/{user_training_id}")
async def get_user_training_menu(user_training_id: str, db: Session=Depends(get_db)):

    training = {}
    user_training_menu_dic = {}
    try:
        # トレーニングプランの詳細を取得する
        result = crud_get_user_training_menu(db=db, user_training_id=user_training_id)
        for r in result:
            training_name = r.training_name
            description = r.description
            sets = r.sets
            reps = r.reps
            kgs = r.kgs
            training = {
                'training_name': training_name,
                'description': description,
                'sets': sets,
                'reps': reps,
                'kgs': kgs
            }

        sets = 0 if sets is None else sets
        for i in range(1, int(sets) + 1):
            user_training_menu_dic[i] = {
                "reps": reps,
                "kgs": kgs
            }

        statusCode = 200
        statusMessage = "トレーニングメニューの取得に成功しました。"

    except Exception as e:
        statusCode = 500
        statusMessage = "トレーニングメニューの取得に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "training": training,
        "user_training_menu": user_training_menu_dic
    }
    return JSONResponse(content=content)
