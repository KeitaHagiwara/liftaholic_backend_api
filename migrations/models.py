from sqlalchemy import Column, BOOLEAN, String, INTEGER, FLOAT, TEXT, DATETIME, TIMESTAMP, VARCHAR, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql.functions import current_timestamp

Base = declarative_base()

class BaseModel(Base):
    """ ベースモデル
    """
    __abstract__ = True

    id = Column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )

    created_at = Column(
        'created_at',
        TIMESTAMP(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
        comment='登録日時',
    )

    updated_at = Column(
        'updated_at',
        TIMESTAMP(timezone=True),
        onupdate=current_timestamp(),
        comment='最終更新日時',
    )

    # @declared_attr
    # def __mapper_args__(cls):
    #     """ デフォルトのオーダリングは主キーの昇順

    #     降順にしたい場合
    #     from sqlalchemy import desc
    #     # return {'order_by': desc('id')}
    #     """
    #     return {'order_by': 'id'}

class tUsers(BaseModel):
    __tablename__ = 't_users'

    user_id = Column(TEXT, unique=True, nullable=False)
    # last_name = Column(VARCHAR(100), nullable=True)
    # first_name = Column(VARCHAR(100), nullable=True)
    ## icon = image_attachment('tUserIcon')
    # tel = Column(VARCHAR(100), nullable=True)
    # postal_code = Column(VARCHAR(8), nullable=True)
    # prefecture_id = Column(INTEGER, ForeignKey('m_prefectures.prefecture_id'), nullable=True)
    # point_possessed = Column(INTEGER, nullable=False, default=0)
    id_admin = Column(BOOLEAN, nullable=False, default=False)
    is_active = Column(BOOLEAN, nullable=False, default=True)

# class tUserIcon(Base, Image):
#     __tablename__ = 't_user_icon'

#     user_id = Column(INTEGER, ForeignKey('t_users.id'), primary_key=True)
#     user = relationship('tUsers')

class tTrainingPlans(BaseModel):
    __tablename__ = 't_training_plans'

    user_id = Column(String, ForeignKey('t_users.user_id'))
    training_plan_name = Column(VARCHAR(100), nullable=False)
    training_plan_description = Column(TEXT, nullable=True)

class tUserTrainings(BaseModel):
    __tablename__ = 't_user_trainings'

    training_plan_id = Column(INTEGER, ForeignKey('t_training_plans.id', ondelete='CASCADE'), nullable=False)
    training_no = Column(INTEGER, ForeignKey('m_trainings.training_no'), nullable=False)
    sets = Column(INTEGER, nullable=True)
    reps = Column(INTEGER, nullable=True)
    kgs = Column(FLOAT, nullable=True)
    interval = Column(VARCHAR(5), nullable=True)

class tUserTrainingAchievements(BaseModel):
    __tablename__ = 't_user_training_achievements'

    user_id = Column(TEXT, ForeignKey('t_users.user_id', ondelete='CASCADE'), nullable=False)
    training_plan_id = Column(INTEGER, ForeignKey('t_training_plans.id'), nullable=False)
    training_no = Column(INTEGER, ForeignKey('m_trainings.training_no'), nullable=False)
    reps_achieve = Column(INTEGER, nullable=False)
    kgs_achieve = Column(FLOAT, nullable=False)
    time_elapsed = Column(VARCHAR(5), nullable=False)

class tUserCalendars(BaseModel):
    __tablename__ = 't_user_calendars'

    user_id = Column(String, ForeignKey('t_users.user_id'))
    event_name = Column(VARCHAR(100), nullable=False)
    event_datetime = Column(TIMESTAMP, nullable=False)
    training_plan_id = Column(INTEGER, ForeignKey('t_training_plans.id'), nullable=True)
    calendar_comment = Column(TEXT, nullable=True)

class tNotifications(BaseModel):
    __tablename__ = 't_notifications'

    user_id = Column(String, ForeignKey('t_users.user_id'), nullable=True)
    title = Column(VARCHAR(255), nullable=False)
    detail = Column(TEXT, nullable=False)
    type = Column(INTEGER, nullable=False, default=0)
    is_read = Column(BOOLEAN, nullable=True, default=False)

# ----------------------------------------------------
# マスタ系
# ----------------------------------------------------
class mPrefectures(Base):
    __tablename__ = 'm_prefectures'

    prefecture_id = Column(INTEGER, primary_key=True)
    prefecture_name = Column(VARCHAR(10), nullable=False)

class mTrainings(Base):
    __tablename__ = 'm_trainings'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    training_no = Column(INTEGER, unique=True, nullable=False)
    training_name = Column(VARCHAR(100), nullable=False)
    description = Column(TEXT, nullable=False)
    purpose_no = Column(INTEGER, ForeignKey('m_purposes.purpose_no'))
    part_no = Column(INTEGER, ForeignKey('m_parts.part_no'))
    type_no = Column(INTEGER, ForeignKey('m_types.type_no'))
    event_no = Column(INTEGER, ForeignKey('m_events.event_no'))
    # effectiveness_no = Column(INTEGER, ForeignKey('m_effectiveness.effectiveness_no'))
    # difficulty_no = Column(INTEGER, ForeignKey('m_difficulty.difficulty_no'))

class mPurposes(Base):
    # 動機、ゴール
    # 例：筋肥大のため、引き締めたいetc
    __tablename__ = 'm_purposes'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    purpose_no = Column(INTEGER, unique=True, nullable=False)
    purpose_name = Column(VARCHAR(100), nullable=False)
    purpose_comment = Column(VARCHAR(100), nullable=True)

class mParts(Base):
    # 部位
    __tablename__ = 'm_parts'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    part_no = Column(INTEGER, unique=True, nullable=False)
    part_name = Column(VARCHAR(100), nullable=False)
    sub_part_name = Column(VARCHAR(100), nullable=False)
    part_comment = Column(VARCHAR(100), nullable=True)
    part_image_file = Column(VARCHAR(255), nullable=True)

class mTypes(Base):
    # タイプ
    # プッシュ or プル
    __tablename__ = 'm_types'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    type_no = Column(INTEGER, unique=True, nullable=False)
    type_name = Column(VARCHAR(100), nullable=False)
    type_comment = Column(VARCHAR(100), nullable=True)

class mEvents(Base):
    # 種目
    # アイソレーション種目 or コンパウンド種目
    __tablename__ = 'm_events'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    event_no = Column(INTEGER, unique=True, nullable=False)
    event_name = Column(VARCHAR(100), nullable=False)
    event_comment = Column(VARCHAR(100), nullable=True)

# class mDifficulty(Base):
#     # 難易度(星で5段階)
#     __tablename__ = 'm_difficulty'

#     id = Column(INTEGER, primary_key=True)
#     difficulty_no = Column(INTEGER, unique=True, nullable=False)
#     difficulty_rank = Column(INTEGER, nullable=False)
#     difficulty_name = Column(VARCHAR(100), nullable=False)

# class mEffectiveness(Base):
#     # 効果性(星で5段階)
#     __tablename__ = 'm_effectiveness'

#     id = Column(INTEGER, primary_key=True)
#     effectiveness_no = Column(INTEGER, unique=True, nullable=False)
#     effectiveness_rank = Column(INTEGER, nullable=False)
#     effectiveness_name = Column(VARCHAR(100), nullable=False)
