from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os, sys, datetime, time
sys.path.append(os.pardir)

from db.database import get_db
# select系
from crud.crud import crud_get_user_training_data, crud_get_all_trainings
# insert系
# from crud.crud import
# update系
from crud.crud import crud_update_training_plan
# delete系
# from crud.crud import

router = APIRouter(
    prefix='/api/workout',
    tags=['workout']
)

class UpdateTrainingPlan(BaseModel):
    user_id: str
    training_plan_id: str
    training_title: str
    training_description: str

# ----------------------------------------
# ユーザーのトレーニングデータを取得する
# ----------------------------------------
@router.get("/get_user_training_data/{uid}")
async def workout_init(uid: str, db: Session=Depends(get_db)):
    training_plans = []

    try:
        # ユーザーのトレーニングプランを取得する
        result = crud_get_user_training_data(db=db, uid=uid)
        user_training_menu = {}
        for r in result:
            if r.training_plan_id not in user_training_menu:
                user_training_menu[r.training_plan_id] = {
                    "training_plan_name": r.training_plan_name,
                    "training_plan_description": r.training_plan_description,
                    "count": 1 if r.user_training_id is not None else 0,
                    "training_menu": {
                        r.user_training_id: {
                            "training_name": r.training_name,
                            "description": r.description,
                            "sets": r.sets if r.sets is not None else 1,
                            "reps": r.reps if r.reps is not None else 1,
                            "kgs": r.kgs if r.kgs is not None else 0.25,
                        }
                    } if r.user_training_id is not None else {}
                }
            else:
                user_training_menu[r.training_plan_id]["training_menu"][r.user_training_id] = {
                    "training_name": r.training_name,
                    "description": r.description,
                    "sets": r.sets if r.sets is not None else 1,
                    "reps": r.reps if r.reps is not None else 1,
                    "kgs": r.kgs if r.kgs is not None else 0.25,
                }
                user_training_menu[r.training_plan_id]["count"] = len(user_training_menu[r.training_plan_id]["training_menu"])

            print(user_training_menu)

        statusCode = 200
        statusMessage = "ユーザーのトレーニングデータを取得しました。"

    except Exception as e:

        statusCode = 500
        statusMessage = "ユーザーのトレーニングデータの取得に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "training_plans": user_training_menu,
    }
    return JSONResponse(content=content)

# ----------------------------------------
# 全トレーニングメニューのマスタを取得する
# ----------------------------------------
@router.get("/get_all_training_menu_master")
async def get_all_training_menu_master(db: Session=Depends(get_db)):
    try:
        result = crud_get_all_trainings(db=db)
        training_menu = {}
        for r in result:
            training_no = r.training_no
            parts = r.part_name
            elm_dic = {
                "training_name": r.training_name,
                "description": r.description,
                "purpose_name": r.purpose_name,
                "purpose_comment": r.purpose_comment,
                "sub_part_name": r.sub_part_name,
                "type_name": r.type_name,
                "type_comment": r.type_comment,
                "event_name": r.event_name,
                "event_comment": r.event_comment
            }
            if parts not in training_menu:
                training_menu[parts] = {}

            training_menu[parts][training_no] = elm_dic

        statusCode = 200
        statusMessage = "トレーニングメニューマスタを取得しました。"

    except Exception as e:
        statusCode = 500
        statusMessage = "トレーニングメニューマスタの取得に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "training_menu": training_menu,
    }
    return JSONResponse(content=content)

# ----------------------------------------
# トレーニングプランを編集する
# ----------------------------------------
@router.post("/update_training_plan")
async def customize_user_trainings(request: UpdateTrainingPlan, db: Session=Depends(get_db)):
    results = None
    try:
        crud_update_training_plan(
            db=db,
            user_id=request.user_id,
            training_plan_id=request.training_plan_id,
            training_title=request.training_title,
            training_description=request.training_description,
        )

        statusCode = 200
        statusMessage = "トレーニングプランを更新しました。"

    except Exception as e:
        statusCode = 500
        statusMessage = "トレーニングプランの更新に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage
    }
    return content