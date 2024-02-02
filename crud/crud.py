from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import asc, desc
from fastapi.responses import JSONResponse
import os, sys

sys.path.append(os.pardir)
from migrations.models import tUsers, tTrainingPlans, tUserTrainings, tNotifications

# サインアップで新規ユーザーを追加する
def create_user_if_not_exists(db: Session, user_id):
    try:
        user_obj = db.query(tUsers).filter(tUsers.user_id == user_id).first()
        print(user_obj)
        # ユーザーが登録されていない場合は追加する
        if user_obj is None:
            user = tUsers(
                user_id = user_id
            )
            db.add(user)
            db.commit()
            user_obj = db.query(tUsers).filter(tUsers.user_id == user_id).first()

        status_code = 200
        status_msg = 'Success'

    except Exception as e:
        status_code = 500
        status_msg = 'Error'

    context = {'status_code': status_code, 'status_msg': status_msg}
    return context

# ユーザーのトレーニングプランを取得する
def get_user_training_plan(db: Session, user_id):
    statement = text("""
                    SELECT
                        tp.training_plan_name,
                        tp.training_plan_description,
                        count(ut.training_plan_id) as count
                    FROM t_training_plans as tp
                    LEFT OUTER JOIN t_user_trainings as ut
                    ON tp.id = ut.training_plan_id
                    WHERE tp.user_id = :user_id
                    GROUP BY tp.id
                    """)

    result = db.execute(statement, [{"user_id": user_id}])
    return result

# def get_user_trainings(db: Session, user_id):
#     return db.query(models.tTrainingPlans).join(models.tUserTrainings).filter(models.tTrainingPlans.user_id == user_id).all()

def create_training_plan(db: Session, user_id, training_title, training_description):
    training_obj = tTrainingPlans(
        user_id = user_id,
        training_plan_name = training_title,
        training_plan_description = training_description
    )
    db.add(training_obj)
    db.commit()

    return db.get(tTrainingPlans, training_obj.id)


# お知らせを全て取得する
def get_all_notifications(db: Session):

    return db.query(tNotifications).order_by(asc(tNotifications.id)).all()



