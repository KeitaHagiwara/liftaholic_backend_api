from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os, sys
sys.path.append(os.pardir)
from db.database import get_db
from crud.crud import get_user_training_plan, create_training_plan


router = APIRouter(
    prefix='/api/training_plan',
    tags=['planning']
)

# リクエストbodyを定義
class TrainingPlan(BaseModel):
    user_id: str
    training_title: str
    training_description: str


@router.get("/{uid}")
async def planning_init(uid: str, db: Session=Depends(get_db)):
    result = get_user_training_plan(db=db, user_id=uid)
    training_plans = []
    for r in result:
        training_plans.append(
            {
                "training_title": r.training_plan_name,
                "training_description": r.training_plan_description,
                "training_counts": r.count
            }
        )
    content = {
        'training_plans': training_plans
    }
    return JSONResponse(content=content)

# usersを新規登録する
@router.post("/create_training_plan", tags=["create_training_plan"])
async def create_user(request: TrainingPlan, db: Session=Depends(get_db)):
    result = create_training_plan(
        db=db,
        user_id=request.user_id,
        training_title=request.training_title,
        training_description=request.training_description
    )

    return {'result': result}