from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os, sys, datetime
sys.path.append(os.pardir)
from db.database import get_db
# select系
from crud.crud import crud_get_user_training_plan, crud_get_user_calendar, crud_get_all_trainings, crud_get_training_plan_menu
# insert系
from crud.crud import crud_create_training_plan, crud_add_training_menu
# delete系


router = APIRouter(
    prefix='/api/training_plan',
    tags=['planning']
)

# リクエストbodyを定義
class TrainingPlan(BaseModel):
    user_id: str
    training_title: str
    training_description: str

class TrainingMenu(BaseModel):
    training_plan_id: int
    training_no: int

# ------------------------------------------------
# select系
# ------------------------------------------------
@router.get("/get_user_training_plans/{uid}")
async def planning_init(uid: str, db: Session=Depends(get_db)):
    # ユーザーのトレーニングプランを取得する
    result_tp = crud_get_user_training_plan(db=db, user_id=uid)
    training_plans = []
    for r in result_tp:
        training_plans.append(
            {
                "training_plan_id": r.id,
                "training_title": r.training_plan_name,
                "training_description": r.training_plan_description,
                "training_counts": r.count
            }
        )
    # ユーザーのトレーニングカレンダーを取得する
    result_tc = crud_get_user_calendar(db=db, user_id=uid)
    # format
    # calendar_events = [
    #     {'ce_year': 2024, 'ce_month': 2, 'ce_day': 14, 'event_list': ['event1', 'event2'], 'training_plan_list': [1]},
    #     {'ce_year': 2024, 'ce_month': 2, 'ce_day': 18, 'event_list': ['event3', 'event4', 'event5'], 'training_plan_list': []},
    # ]

    calendar_events = []
    calendar_dict = {}
    event_list = []
    training_plan_list = []
    for r in result_tc:
        event_name = r.event_name
        event_datetime = str(r.event_datetime)
        training_plan_id = r.training_plan_id

        d = datetime.datetime.strptime(event_datetime, '%Y-%m-%d %H:%M:%S')
        d_key = str(d.year) + '-' + str(d.month) + '-' + str(d.day)
        if d_key not in calendar_dict:
            calendar_dict[d_key] = {'event_list': [event_name], 'training_plan_list': []}
            if training_plan_id is not None:
                calendar_dict[d_key]['training_plan_list'].append(training_plan_id)
        else:
            calendar_dict[d_key]['event_list'].append(event_name)
            if training_plan_id is not None:
                calendar_dict[d_key]['training_plan_list'].append(training_plan_id)

    for key, val in calendar_dict.items():
        d_key_list = key.split('-')
        calendar_events.append({
            'ce_year': int(d_key_list[0]),
            'ce_month': int(d_key_list[1]),
            'ce_day': int(d_key_list[2]),
            'event_list': val['event_list'],
            'training_plan_list': val['training_plan_list'],
        })

    content = {
        'training_plans': training_plans,
        'calendar_events': calendar_events
    }
    return JSONResponse(content=content)

@router.get("/get_registered_trainings/{training_plan_id}")
async def get_training_plan_menu(training_plan_id: int, db: Session=Depends(get_db)):
    # ユーザーのトレーニングプランを取得する
    result = crud_get_training_plan_menu(db=db, training_plan_id=training_plan_id)
    user_training_menu = []
    for r in result:
        user_training_menu.append(
            {
                "user_training_id": r.id,
                "training_name": r.training_name,
                "description": r.description,
            }
        )

    content = {
        'user_training_menu': user_training_menu
    }
    return JSONResponse(content=content)

@router.get("/get_all_training_menu")
async def get_all_training_menu(db: Session=Depends(get_db)):
    # 全てトレーニングプランを取得する
    result = crud_get_all_trainings(db=db)
    training_menu = {}
    for r in result:
        training_no = r.training_no
        parts = r.part_name
        elm_dic = {
            'training_name': r.training_name,
            'description': r.description,
            'purpose_name': r.purpose_name,
            'purpose_comment': r.purpose_comment,
            'sub_part_name': r.sub_part_name,
            'type_name': r.type_name,
            'type_comment': r.type_comment,
            'event_name': r.event_name,
            'event_comment': r.event_comment
        }
        if parts not in training_menu:
            training_menu[parts] = {}

        training_menu[parts][training_no] = elm_dic

    content = {
        'training_menu': training_menu,
    }
    return JSONResponse(content=content)


# ------------------------------------------------
# insert系
# ------------------------------------------------
# トレーニングプランにメニューを追加する
@router.post("/add_training_menu", tags=["add_training_menu"])
async def add_training_menu(request: TrainingMenu, db: Session=Depends(get_db)):
    result = crud_add_training_menu(
        db=db,
        training_plan_id=request.training_plan_id,
        training_no=request.training_no
    )
    print(result)
    return {'result': result}

# usersを新規登録する
@router.post("/create_training_plan", tags=["create_training_plan"])
async def create_user(request: TrainingPlan, db: Session=Depends(get_db)):

    result = crud_create_training_plan(
        db=db,
        user_id=request.user_id,
        training_title=request.training_title,
        training_description=request.training_description
    )
    print(result)
    return {'result': result}