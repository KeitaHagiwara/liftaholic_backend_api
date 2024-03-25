from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os, sys, datetime, time
sys.path.append(os.pardir)
from db.database import get_db
# select系
from crud.crud import crud_get_user_training_data, crud_get_user_calendar, crud_get_all_trainings
# insert系
from crud.crud import crud_create_training_plan, crud_add_training_menu, crud_customize_user_trainings
# delete系
from crud.crud import crud_delete_user_training_menu, crud_delete_user_training_plan

router = APIRouter(
    prefix="/api/training_plan",
    tags=["planning"]
)

# リクエストbodyを定義
class TrainingPlan(BaseModel):
    user_id: str
    training_title: str
    training_description: str

class TrainingMenu(BaseModel):
    training_plan_id: int
    training_no: int

class CustomizedTrainings(BaseModel):
    user_training_id: int
    sets: int
    reps: int
    kgs: float

# ------------------------------------------------
# select系
# ------------------------------------------------
@router.get("/get_user_training_plans/{uid}")
async def planning_init(uid: str, db: Session=Depends(get_db)):
    training_plans = []
    calendar_events = []

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
                            "sets": r.sets,
                            "reps": r.reps,
                            "kgs": r.kgs
                        }
                    } if r.user_training_id is not None else {}
                }
            else:
                user_training_menu[r.training_plan_id]["training_menu"][r.user_training_id] = {
                    "training_name": r.training_name,
                    "description": r.description,
                    "sets": r.sets,
                    "reps": r.reps,
                    "kgs": r.kgs
                }
                user_training_menu[r.training_plan_id]["count"] = len(user_training_menu[r.training_plan_id]["training_menu"])


        # ユーザーのトレーニングカレンダーを取得する
        result_tc = crud_get_user_calendar(db=db, user_id=uid)
        # format
        # calendar_events = [
        #     {"ce_year": 2024, "ce_month": 2, "ce_day": 14, "event_list": ["event1", "event2"], "training_plan_list": [1]},
        #     {"ce_year": 2024, "ce_month": 2, "ce_day": 18, "event_list": ["event3", "event4", "event5"], "training_plan_list": []},
        # ]

        calendar_events = []
        calendar_dict = {}
        event_list = []
        training_plan_list = []
        for r in result_tc:
            event_name = r.event_name
            event_datetime = str(r.event_datetime)
            training_plan_id = r.training_plan_id

            d = datetime.datetime.strptime(event_datetime, "%Y-%m-%d %H:%M:%S")
            d_key = str(d.year) + "-" + str(d.month) + "-" + str(d.day)
            if d_key not in calendar_dict:
                calendar_dict[d_key] = {"event_list": [event_name], "training_plan_list": []}
                if training_plan_id is not None:
                    calendar_dict[d_key]["training_plan_list"].append(training_plan_id)
            else:
                calendar_dict[d_key]["event_list"].append(event_name)
                if training_plan_id is not None:
                    calendar_dict[d_key]["training_plan_list"].append(training_plan_id)

        for key, val in calendar_dict.items():
            d_key_list = key.split("-")
            calendar_events.append({
                "ce_year": int(d_key_list[0]),
                "ce_month": int(d_key_list[1]),
                "ce_day": int(d_key_list[2]),
                "event_list": val["event_list"],
                "training_plan_list": val["training_plan_list"],
            })

        statusCode = 200
        statusMessage = "トレーニングプランを取得しました。"

    except Exception as e:

        statusCode = 500
        statusMessage = "トレーニングプランの取得に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "training_plans": user_training_menu,
        "calendar_events": calendar_events
    }
    return JSONResponse(content=content)

# ------------------------------------------------
# insert系
# ------------------------------------------------
# トレーニングプランにメニューを追加する
@router.post("/add_training_menu", tags=["add_training_menu"])
async def add_training_menu(request: TrainingMenu, db: Session=Depends(get_db)):
    add_user_training_id = None
    add_data = {}
    try:
        add_result = crud_add_training_menu(
            db=db,
            training_plan_id=request.training_plan_id,
            training_no=request.training_no
        )

        if (add_result["is_registered"]):
            statusCode = 409
            statusMessage = "該当のメニューは既にプランに登録済みです。"

        else:
            for r in add_result["result"]:
                add_user_training_id = r.user_training_id,
                add_data["training_name"] = r.training_name
                add_data["description"] = r.description
                add_data["sets"] = 1
                add_data["reps"] = 1
                add_data["kgs"] = 0.25

            statusCode = 200
            statusMessage = r.training_name + "をトレーニングメニューを追加しました。"

    except Exception as e:
        statusCode = 500
        statusMessage = "トレーニングメニューの追加に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "add_user_training_id": add_user_training_id,
        "add_data": add_data,
    }
    return content

# トレーニングプランを新規作成する
@router.post("/create_training_plan", tags=["create_training_plan"])
async def create_training_plan(request: TrainingPlan, db: Session=Depends(get_db)):
    results = None
    try:
        result = crud_create_training_plan(
            db=db,
            user_id=request.user_id,
            training_title=request.training_title,
            training_description=request.training_description
        )

        statusCode = 200
        statusMessage = "トレーニングプランを新規作成しました。"

    except Exception as e:
        statusCode = 500
        statusMessage = "トレーニングプランの新規作成に失敗しました。"

    content = {
        "statusCode": statusCode,
        "statusMessage": statusMessage,
        "result": result,
    }
    return content

# set/reps/kgを設定する
@router.post("/customize_user_trainings", tags=["create_training_plan"])
async def customize_user_trainings(request: CustomizedTrainings, db: Session=Depends(get_db)):
    results = None
    try:
        crud_customize_user_trainings(
            db=db,
            user_training_id=request.user_training_id,
            sets=request.sets,
            reps=request.reps,
            kgs=request.kgs,
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


# ------------------------------------------------
# delete系
# ------------------------------------------------
@router.delete("/delete_user_training_menu/{user_training_id}")
async def delete_user_training_menu(user_training_id: int, db: Session=Depends(get_db)):
    # DBから該当のデータを削除する
    try:
        crud_delete_user_training_menu(db=db, user_training_id=user_training_id)
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

@router.delete("/delete_training_plan/{training_plan_id}")
async def delete_user_training_plan(training_plan_id: int, db: Session=Depends(get_db)):
    # DBから該当のデータを削除する
    try:
        crud_delete_user_training_plan(db=db, training_plan_id=training_plan_id)

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