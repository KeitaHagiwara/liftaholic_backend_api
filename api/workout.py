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
from crud.crud import crud_insert_training_set_achieved
# update系
from crud.crud import crud_update_training_plan, crud_upsert_training_menus, crud_update_training_set
# delete系
from crud.crud import crud_delete_user_training_plan, crud_delete_user_training_menu

router = APIRouter(
    prefix='/api/workout',
    tags=['workout']
)

class UpdateTrainingPlan(BaseModel):
    user_id: str
    training_plan_id: str
    training_title: str
    training_description: str

class UpdateTrainingMenu(BaseModel):
    user_id: str
    training_plan_id: str
    training_master: object

class UpdateTrainingSet(BaseModel):
    user_id: str
    user_training_id: int
    sets: int
    reps: int
    kgs: float
    interval: str

class AchievedTrainingSet(BaseModel):
    user_id: str
    training_plan_id: str
    training_set_achieved: object

# ----------------------------------------
# ユーザーのトレーニングデータを取得する
# ----------------------------------------
@router.get("/get_user_training_data/{uid}")
async def workout_init(uid: str, db: Session=Depends(get_db)):

    try:
        # ユーザーのトレーニングデータを取得する
        user_training_menu = get_user_training_data(db, uid)
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

def get_user_training_data(db, uid):
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
                        "part_name": r.part_name,
                        "part_image_file": r.part_image_file,
                        "type_name": r.type_name,
                        "event_name": r.event_name,
                        "sets": r.sets if r.sets is not None else 3,
                        "reps": r.reps if r.reps is not None else 1,
                        "kgs": r.kgs if r.kgs is not None else 0.25,
                        "interval": r.interval if r.interval is not None else "01:00",
                    }
                } if r.user_training_id is not None else {}
            }
        else:
            user_training_menu[r.training_plan_id]["training_menu"][r.user_training_id] = {
                "training_name": r.training_name,
                "description": r.description,
                "part_name": r.part_name,
                "part_image_file": r.part_image_file,
                "type_name": r.type_name,
                "event_name": r.event_name,
                "sets": r.sets if r.sets is not None else 3,
                "reps": r.reps if r.reps is not None else 1,
                "kgs": r.kgs if r.kgs is not None else 0.25,
                "interval": r.interval if r.interval is not None else "01:00",
            }
            user_training_menu[r.training_plan_id]["count"] = len(user_training_menu[r.training_plan_id]["training_menu"])

    return user_training_menu


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
                "is_selected": False,
                "training_name": r.training_name,
                "description": r.description,
                "purpose_name": r.purpose_name,
                "purpose_comment": r.purpose_comment,
                "part_name": r.part_name,
                "sub_part_name": r.sub_part_name,
                "part_image_file": r.part_image_file,
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
async def customize_training_plan(request: UpdateTrainingPlan, db: Session=Depends(get_db)):
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

# ----------------------------------------
# トレーニングメニューを更新する
# ----------------------------------------
@router.post("/update_training_menu")
async def update_training_menu(request: UpdateTrainingMenu, db: Session=Depends(get_db)):

    user_id = request.user_id
    training_plan_id = request.training_plan_id,
    training_menu = request.training_master

    try:
        crud_upsert_training_menus(db, user_id, training_plan_id, training_menu)
        user_training_data = get_user_training_data(db, user_id)
        statusCode = 200
        statusMessage = "トレーニングメニューを更新しました。"

    except Exception as e:
        statusCode = 500
        statusMessage = "トレーニングメニューの追加に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "user_training_data": user_training_data,
    }
    return content

# ----------------------------------------
# トレーニングセットを編集する
# set/reps/kg/セット間インターバル
# ----------------------------------------
@router.post("/update_training_set")
async def customize_training_set(request: UpdateTrainingSet, db: Session=Depends(get_db)):
    results = None
    try:
        crud_update_training_set(
            db=db,
            user_id = request.user_id,
            user_training_id=request.user_training_id,
            sets=request.sets,
            reps=request.reps,
            kgs=request.kgs,
            interval = request.interval,
        )

        statusCode = 200
        statusMessage = "トレーニングメニューを更新しました。"

    except Exception as e:
        statusCode = 500
        statusMessage = "トレーニングメニューの更新に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage
    }
    return content

# ----------------------------------------
# トレーニングプランを削除する
# ----------------------------------------
@router.delete("/delete_training_plan/{user_id}/{training_plan_id}")
async def delete_user_training_plan(user_id: str, training_plan_id: int, db: Session=Depends(get_db)):
    # DBから該当のデータを削除する
    try:
        crud_delete_user_training_plan(db=db, user_id=user_id, training_plan_id=training_plan_id)

        statusCode = 200
        statusMessage = "トレーニングプランを削除しました。"

    except Exception as e:

        statusCode = 500
        statusMessage = "トレーニングプランの削除に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "deleted_id": training_plan_id
    }
    return JSONResponse(content=content)

# ----------------------------------------
# トレーニングメニューを削除する
# ----------------------------------------
@router.delete("/delete_user_training_menu/{user_id}/{user_training_id}")
async def delete_user_training_menu(user_id: str, user_training_id: int, db: Session=Depends(get_db)):
    # DBから該当のデータを削除する
    try:
        crud_delete_user_training_menu(db=db, user_id=user_id, user_training_id=user_training_id)
        statusCode = 200
        statusMessage = "トレーニングメニューを削除しました。"
    except Exception as e:
        statusCode = 500
        statusMessage = "トレーニングメニューの削除に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage
    }
    return JSONResponse(content=content)

# ----------------------------------------
# ワークアウト完了時に実績をDBに保存する
# ----------------------------------------
@router.post("/complete_workout")
async def complete_workout(request: AchievedTrainingSet, db: Session=Depends(get_db)):
    user_id = request.user_id
    training_plan_id = request.training_plan_id
    set_achieved = request.training_set_achieved

    print(user_id)
    print(training_plan_id)
    print(set_achieved)

    try:
        crud_insert_training_set_achieved(
            db=db,
            user_id=user_id,
            training_plan_id=training_plan_id,
            set_achieved=set_achieved
        )
        statusCode = 200
        statusMessage = "ワークアウトが完了しました。\nお疲れ様でした！"


    except Exception as e:
        statusCode = 500
        statusMessage = "ワークアウト実績の登録に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage
    }
    return content
