from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os, sys, datetime, time
sys.path.append(os.pardir)
from db.database import get_db
# select系
from crud.crud import crud_get_user_training_data, crud_get_user_calendar
# insert系
from crud.crud import crud_create_training_plan
# delete系
# from crud.crud import

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
    user_id: str
    training_plan_id: int
    training_no: int

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

# ------------------------------------------------
# delete系
# ------------------------------------------------

