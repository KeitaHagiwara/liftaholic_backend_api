from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import asc, desc, and_, or_
from fastapi.responses import JSONResponse
import os, sys

sys.path.append(os.pardir)
from migrations.models import tUsers, tTrainingPlans, tUserTrainings, tUserCalendars, tNotifications, mTrainings

NOTIFICATION_TYPE = [99]

# ------------------------
# 新規ユーザー追加用のCRUD
# ------------------------
# サインアップで新規ユーザーを追加する
def create_user_if_not_exists(db: Session, user_id):
    user_obj = db.query(tUsers).filter(tUsers.user_id == user_id).first()
    # ユーザーが登録されていない場合は追加する
    if user_obj is None:
        user = tUsers(
            user_id = user_id
        )
        db.add(user)
        db.commit()
        user_obj = db.query(tUsers).filter(tUsers.user_id == user_id).first()

    return user_obj

# ------------------------
# プランニング画面用のCRUD
# ------------------------
# ユーザーの全トレーニングプランを取得する
def crud_get_all_user_training_plan(db: Session, user_id):
    statement = text("""
                    SELECT
                        tp.id,
                        tp.training_plan_name,
                        tp.training_plan_description,
                        count(ut.training_plan_id) as count
                    FROM t_training_plans as tp
                    LEFT OUTER JOIN t_user_trainings as ut
                    ON tp.id = ut.training_plan_id
                    WHERE tp.user_id = :user_id
                    GROUP BY tp.id
                    ORDER BY tp.created_at ASC
                    """)

    result = db.execute(statement, [{"user_id": user_id}])
    return result

# ユーザーのトレーニングプランを取得する
def crud_get_user_training_plan(db: Session, training_plan_id):
    return db.get(tTrainingPlans, training_plan_id)

# ユーザーのトレーニングプランに登録済みのトレーニングメニューの一覧を取得する
def crud_get_training_plan_menu(db: Session, training_plan_id):
    statement = text("""
                SELECT
                    ut.id AS id,
                    ut.training_plan_id AS training_plan_id,
                    ut.training_no AS training_no,
                    tr.training_name AS training_name,
                    tr.description AS description,
                    ut.sets AS sets,
                    ut.reps AS reps,
                    ut.kgs AS kgs
                FROM t_user_trainings as ut
                LEFT OUTER JOIN m_trainings as tr
                ON ut.training_no = tr.training_no
                WHERE ut.training_plan_id = :training_plan_id
                """)

    result = db.execute(statement, [{"training_plan_id": training_plan_id}])
    return result

# ユーザーのカレンダーを取得する
def crud_get_user_calendar(db: Session, user_id):
    return db.query(tUserCalendars).filter(tUserCalendars.user_id==user_id).all()

def crud_delete_user_training_menu(db: Session, user_training_id):
    # 削除対象のメニューを検索
    tgt_user_training = db.get(tUserTrainings, user_training_id)
    # 指定のデータを削除
    db.delete(tgt_user_training)
    db.commit()

def crud_delete_user_training_plan(db: Session, training_plan_id):
    # 削除対象のプランを検索
    tgt_training_plan = db.get(tTrainingPlans, training_plan_id)
    # 指定のデータを削除
    db.delete(tgt_training_plan)
    db.commit()

# 全トレーニングメニューを取得する
def crud_get_all_trainings(db: Session):
    statement = text("""
                SELECT
                    tr.training_no AS training_no,
                    tr.training_name AS training_name,
                    tr.description AS description,
                    pu.purpose_name AS purpose_name,
                    pu.purpose_comment AS purpose_comment,
                    pa.part_name AS part_name,
                    pa.sub_part_name AS sub_part_name,
                    ty.type_name AS type_name,
                    ty.type_comment AS type_comment,
                    ev.event_name AS event_name,
                    ev.event_comment AS event_comment
                FROM m_trainings as tr
                JOIN m_purposes AS pu
                    ON tr.purpose_no = pu.purpose_no
                JOIN m_parts AS pa
                    ON tr.part_no = pa.part_no
                JOIN m_types AS ty
                    ON tr.type_no = ty.type_no
                JOIN m_events AS ev
                    ON tr.event_no = ev.event_no
                """)
    result = db.execute(statement)
    return result
    # return db.query(mTrainings).all()

# ユーザーのトレーニングプランにトレーニングメニューを追加する
def crud_add_training_menu(db: Session, training_plan_id, training_no):

    is_registered = True

    user_training_obj = db.query(tUserTrainings)\
                            .filter(tUserTrainings.training_plan_id == training_plan_id, tUserTrainings.training_no == training_no).first()

    # 未登録の場合はinsertする
    if user_training_obj is None:
        is_registered = False
        user_training_obj = tUserTrainings(
            training_plan_id = training_plan_id,
            training_no = training_no
        )
        db.add(user_training_obj)
        db.commit()

    statement = text("""
            SELECT
                ut.id AS user_training_id,
                tr.training_name AS training_name,
                tr.description AS description,
            FROM t_user_trainings as ut
            LEFT OUTER JOIN m_trainings as tr
            ON ut.training_no = tr.training_no
            WHERE ut.id = :user_training_id
            """)
    result = db.execute(statement, [{"user_training_id": user_training_obj.id}])

    content = {
        'is_registered': is_registered,
        'result': result
    }
    return content

# トレーニングプランを新規作成する
def crud_create_training_plan(db: Session, user_id, training_title, training_description):
    training_obj = tTrainingPlans(
        user_id = user_id,
        training_plan_name = training_title,
        training_plan_description = training_description
    )
    db.add(training_obj)
    db.commit()

    return db.get(tTrainingPlans, training_obj.id)

def crud_customize_user_trainings(db: Session, user_training_id, sets, reps, kgs):
    customized_user_training_obj = db.query(tUserTrainings).filter(tUserTrainings.id==user_training_id).first()
    customized_user_training_obj.sets = sets
    customized_user_training_obj.reps = reps
    customized_user_training_obj.kgs = kgs
    # データを確定
    db.commit()

# ------------------------
# お知らせ画面用のCRUD
# ------------------------
# ニュースを全て取得する
def crud_get_all_notifications(db: Session):
    return db.query(tNotifications)\
        .filter(tNotifications.type == 0)\
            .order_by(desc(tNotifications.created_at)).all()

# あなた宛のお知らせを全て取得する
def crud_get_indiv_notifications(db: Session, user_id):
    return db.query(tNotifications)\
        .filter(and_(or_(tNotifications.user_id == user_id, tNotifications.user_id.is_(None)), tNotifications.type == 1))\
            .order_by(desc(tNotifications.created_at)).all()



