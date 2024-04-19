from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import asc, desc, and_, or_
from sqlalchemy.sql.expression import true, false
from fastapi.responses import JSONResponse
import os, sys

sys.path.append(os.pardir)
from migrations.models import tUsers, tTrainingPlans, tUserTrainings, tUserTrainingAchievements, tUserCalendars, tNotifications, mTrainings

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
    statement = text(
        """
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
        """
    )
    result = db.execute(statement, [{"user_id": user_id}])
    return result

# ユーザーのトレーニングプランに登録済みのトレーニングメニューの一覧を取得する
def crud_get_user_training_data(db: Session, uid):
    statement = text(
        """
        SELECT
            tp.id AS training_plan_id,
            tp.training_plan_name AS training_plan_name,
            tp.training_plan_description AS training_plan_description,
            ut.id AS user_training_id,
            ut.training_no AS training_no,
            tr.training_name AS training_name,
            tr.description AS description,
            pt.part_name AS part_name,
            pt.part_image_file AS part_image_file,
            ev.event_name AS event_name,
            ty.type_name AS type_name,
            ut.sets AS sets,
            ut.reps AS reps,
            ut.kgs AS kgs,
            ut.interval AS interval
        FROM t_training_plans AS tp
        LEFT OUTER JOIN t_user_trainings AS ut
            ON tp.id = ut.training_plan_id
        LEFT OUTER JOIN m_trainings AS tr
            ON ut.training_no = tr.training_no
        LEFT OUTER JOIN m_parts AS pt
            ON tr.part_no = pt.part_no
        LEFT OUTER JOIN m_types AS ty
            ON tr.type_no = ty.type_no
        LEFT OUTER JOIN m_events AS ev
            ON tr.event_no = ev.event_no
        WHERE tp.user_id = :user_id
        ORDER BY tp.created_at ASC;
        """
    )
    result = db.execute(statement, [{"user_id": uid}])
    return result

# ユーザーのカレンダーを取得する
def crud_get_user_calendar(db: Session, user_id):
    return db.query(tUserCalendars).filter(tUserCalendars.user_id==user_id).all()

# ユーザーのトレーニングプランを削除する
def crud_delete_user_training_plan(db: Session, user_id, training_plan_id):
    # 削除対象のプランを検索
    delete_training_plan_obj = db.query(tTrainingPlans).filter(tTrainingPlans.user_id==user_id, tTrainingPlans.id==training_plan_id).first()
    # 指定のデータを削除
    db.delete(delete_training_plan_obj)
    db.commit()

# ユーザーのトレーニングメニューを削除する
def crud_delete_user_training_menu(db: Session, user_id, user_training_id):
    # 削除対象のメニューを検索
    delete_training_menu_obj = db.query(tUserTrainings).join(tTrainingPlans).filter(tTrainingPlans.user_id==user_id, tUserTrainings.id==user_training_id).first()
    # 指定のデータを削除
    db.delete(delete_training_menu_obj)
    db.commit()


# 全トレーニングメニューを取得する
def crud_get_all_trainings(db: Session):
    statement = text(
        """
        SELECT
            tr.training_no AS training_no,
            tr.training_name AS training_name,
            tr.description AS description,
            pu.purpose_name AS purpose_name,
            pu.purpose_comment AS purpose_comment,
            pa.part_name AS part_name,
            pa.sub_part_name AS sub_part_name,
            pa.part_image_file AS part_image_file,
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
        """
    )
    result = db.execute(statement)
    return result
    # return db.query(mTrainings).all()

def crud_upsert_training_menus(db: Session, user_id, training_plan_id, training_menu):
    for parts_val in training_menu.values():
        for training_no, training_master_val in parts_val.items():
            training_name = training_master_val['training_name']
            is_selected = training_master_val['is_selected']

            user_training_obj = db.query(tUserTrainings).join(tTrainingPlans).join(mTrainings).filter(tTrainingPlans.user_id==user_id, tUserTrainings.training_plan_id==training_plan_id, mTrainings.training_name==training_name).first()
            # DBに登録がなく、ユーザーに選択されている場合は新規登録
            if (user_training_obj is None and is_selected):
                user_training_obj = tUserTrainings(
                    training_plan_id = training_plan_id,
                    training_no = training_no
                )
                db.add(user_training_obj)

            # DBに登録済みで、ユーザーに選択されていない場合は削除
            elif(user_training_obj is not None and not is_selected):
                db.delete(user_training_obj)
    db.commit()

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

def crud_update_training_plan(db: Session, user_id, training_plan_id, training_title, training_description):
    training_plan_obj = db.query(tTrainingPlans).filter(tTrainingPlans.user_id==user_id, tTrainingPlans.id==training_plan_id).first()
    training_plan_obj.training_plan_name = training_title
    training_plan_obj.training_plan_description = training_description
    # データを確定
    db.commit()

def crud_update_training_set(db: Session, user_id, user_training_id, sets, reps, kgs, interval):
    training_set_obj = db.query(tUserTrainings).join(tTrainingPlans).filter(tTrainingPlans.user_id==user_id, tUserTrainings.id==user_training_id).first()
    training_set_obj.sets = sets
    training_set_obj.reps = reps
    training_set_obj.kgs = kgs
    training_set_obj.interval = interval
    # データを確定
    db.commit()

# ------------------------
# ワークアウト画面用のCRUD
# ------------------------
def crud_get_user_training_menu(db: Session, user_training_id):
    statement = text(
        """
        SELECT
            ut.id,
            tr.training_name,
            tr.description,
            ut.sets,
            ut.reps,
            ut.kgs
        FROM t_user_trainings as ut
        INNER JOIN m_trainings as tr
        ON ut.training_no = tr.training_no
        WHERE ut.id = :user_training_id
        """
    )

    result = db.execute(statement, [{"user_training_id": user_training_id}])
    return result

def crud_insert_training_set_achieved(db:Session, user_id, training_plan_id, set_achieved):

    for elm in set_achieved:
        # トレーニング名からtraining_noを取得する
        training_name = elm['training_name']
        training_no = db.query(mTrainings).filter(mTrainings.training_name==training_name).first().training_no
        achieved_obj = tUserTrainingAchievements(
            user_id = user_id,
            training_plan_id = training_plan_id,
            training_no = training_no,
            reps_achieve = elm['reps'],
            kgs_achieve = elm['kgs'],
            time_elapsed = elm['time']
        )
        db.add(achieved_obj)
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

def crud_get_unread_notifications_count(db: Session, user_id):
    return db.query(tNotifications)\
        .filter(\
            and_(
                or_(tNotifications.user_id == user_id, tNotifications.user_id.is_(None)),\
                tNotifications.type == 1,\
                tNotifications.is_read.is_not(True)
            )\
        ).count()

def crud_update_unread_check(db: Session, user_id, notification_id):
    notification_obj = db.query(tNotifications)\
        .filter(\
            and_(
                or_(tNotifications.user_id == user_id, tNotifications.user_id.is_(None)),\
                tNotifications.id == notification_id
            )\
        ).first()
    # 個人宛のメッセージのみ更新対象
    if notification_obj.type == 1:
        notification_obj.is_read = True
        # データを確定
        db.commit()
