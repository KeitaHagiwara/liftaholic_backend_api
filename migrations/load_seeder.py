from models import mTrainings, mPurposes, mParts, mTypes, mEvents, mPrefectures
import json
import os, sys

sys.path.append(os.pardir)
import db.database as database

db_session = database.SessionLocal()

# seeder用のjsonをロードする
def load_seeder_json(json_file_path):
    with open(json_file_path) as f:
        seeder_json = json.load(f)
    return seeder_json

# ---------------------------
# マスタ系の項目をloadする
# ---------------------------

# トレーニング
def seeder_trainings():
    seeder_json = load_seeder_json('./seeder/training.json')
    for seeder in seeder_json:
        training_no = int(seeder['training_no'])
        trainingObj = db_session.query(mTrainings).filter(mTrainings.training_no == training_no).first()
        # 新規登録の場合
        if trainingObj is None:
            training = mTrainings(
                training_no=int(seeder['training_no']),
                training_name=str(seeder['training_name']),
                description=str(seeder['description']),
                part_no=int(seeder['part_no']),
                purpose_no=int(seeder['purpose_no']),
                type_no=int(seeder['type_no']),
                event_no=int(seeder['event_no'])
            )
            db_session.add(training)
        # 更新の場合
        else:
            trainingObj.training_no=int(seeder['training_no'])
            trainingObj.training_name=str(seeder['training_name'])
            trainingObj.description=str(seeder['description'])
            trainingObj.part_no=int(seeder['part_no'])
            trainingObj.purpose_no=int(seeder['purpose_no'])
            trainingObj.type_no=int(seeder['type_no'])
            trainingObj.event_no=int(seeder['event_no'])

    db_session.commit()

# 動機、目的、ゴール
def seeder_purposes():
    seeder_json = load_seeder_json('./seeder/purpose.json')
    for seeder in seeder_json:
        purpose_no = int(seeder['purpose_no'])
        purposeObj = db_session.query(mPurposes).filter(mPurposes.purpose_no == purpose_no).first()
        # 新規登録の場合
        if purposeObj is None:
            purpose = mPurposes(
                purpose_no=int(seeder['purpose_no']),
                purpose_name=str(seeder['purpose_name']),
                purpose_comment=str(seeder['purpose_comment'])
            )
            db_session.add(purpose)
        # 更新の場合
        else:
            purposeObj.purpose_no=int(seeder['purpose_no'])
            purposeObj.purpose_name=str(seeder['purpose_name'])
            purposeObj.purpose_comment=str(seeder['purpose_comment'])

    db_session.commit()

# 部位
def seeder_parts():
    seeder_json = load_seeder_json('./seeder/part.json')
    for seeder in seeder_json:
        part_no = int(seeder['part_no'])
        partObj = db_session.query(mParts).filter(mParts.part_no == part_no).first()
        # 新規登録の場合
        if partObj is None:
            part = mParts(
                part_no=int(seeder['part_no']),
                part_name=str(seeder['part_name']),
                sub_part_name=str(seeder['sub_part_name']),
                part_comment=str(seeder['part_comment']),
                part_image_file=str(seeder['part_image_file'])
            )
            db_session.add(part)
        # 更新の場合
        else:
            partObj.part_no=int(seeder['part_no'])
            partObj.part_name=str(seeder['part_name'])
            partObj.sub_part_name=str(seeder['sub_part_name'])
            partObj.part_comment=str(seeder['part_comment'])
            partObj.part_image_file=str(seeder['part_image_file'])

    db_session.commit()

# タイプ
def seeder_types():
    seeder_json = load_seeder_json('./seeder/type.json')
    for seeder in seeder_json:
        type_no = int(seeder['type_no'])
        typeObj = db_session.query(mTypes).filter(mTypes.type_no == type_no).first()
        # 新規登録の場合
        if typeObj is None:
            type = mTypes(
                type_no=int(seeder['type_no']),
                type_name=str(seeder['type_name']),
                type_comment=str(seeder['type_comment'])
            )
            db_session.add(type)
        # 更新の場合
        else:
            typeObj.type_no=int(seeder['type_no'])
            typeObj.type_name=str(seeder['type_name'])
            typeObj.type_comment=str(seeder['type_comment'])

    db_session.commit()

# 種目
def seeder_events():
    seeder_json = load_seeder_json('./seeder/event.json')
    for seeder in seeder_json:
        event_no = int(seeder['event_no'])
        eventObj = db_session.query(mEvents).filter(mEvents.event_no == event_no).first()
        # 新規登録の場合
        if eventObj is None:
            event = mEvents(
                event_no=int(seeder['event_no']),
                event_name=str(seeder['event_name']),
                event_comment=str(seeder['event_comment'])
            )
            db_session.add(event)
        # 更新の場合
        else:
            eventObj.event_no=int(seeder['event_no'])
            eventObj.event_name=str(seeder['event_name'])
            eventObj.event_comment=str(seeder['event_comment'])

    db_session.commit()

# # 難易度
# def seeder_difficulty():
#     seeder_json = load_seeder_json('./seeder/difficulty.json')
#     for seeder in seeder_json:
#         difficulty_no = int(seeder['difficulty_no'])
#         difficultyObj = db_session.query(mDifficulty).filter(mDifficulty.difficulty_no == difficulty_no).first()
#         # 新規登録の場合
#         if difficultyObj is None:
#             difficulty = mDifficulty(
#                 difficulty_no=int(seeder['difficulty_no']),
#                 difficulty_rank=int(seeder['difficulty_rank']),
#                 difficulty_name=str(seeder['difficulty_name'])
#             )
#             db_session.add(difficulty)
#         # 更新の場合
#         else:
#             difficultyObj.difficulty_no=int(seeder['difficulty_no'])
#             difficultyObj.difficulty_rank=int(seeder['difficulty_rank'])
#             difficultyObj.difficulty_name=str(seeder['difficulty_name'])

#     db_session.commit()

# # 効果性
# def seeder_effectiveness():
#     seeder_json = load_seeder_json('./seeder/effectiveness.json')
#     for seeder in seeder_json:
#         effectiveness_no = int(seeder['effectiveness_no'])
#         effectivenessObj = db_session.query(mEffectiveness).filter(mEffectiveness.effectiveness_no == effectiveness_no).first()
#         # 新規登録の場合
#         if effectivenessObj is None:
#             effectiveness = mEffectiveness(
#                 effectiveness_no=int(seeder['effectiveness_no']),
#                 effectiveness_rank=int(seeder['effectiveness_rank']),
#                 effectiveness_name=str(seeder['effectiveness_name'])
#             )
#             db_session.add(effectiveness)
#         # 更新の場合
#         else:
#             effectivenessObj.effectiveness_no=int(seeder['effectiveness_no'])
#             effectivenessObj.effectiveness_rank=int(seeder['effectiveness_rank'])
#             effectivenessObj.effectiveness_name=str(seeder['effectiveness_name'])

#     db_session.commit()

# 都道府県
def seeder_prefectures():
    seeder_json = load_seeder_json('./seeder/prefectures.json')
    for seeder in seeder_json:
        prefecture_id = int(seeder['prefecture_id'])
        prefectureObj = db_session.query(mPrefectures).filter(mPrefectures.prefecture_id == prefecture_id).first()
        # 新規登録の場合
        if prefectureObj is None:
            prefecture = mPrefectures(
                prefecture_id=int(seeder['prefecture_id']),
                prefecture_name=str(seeder['prefecture_name'])
            )
            db_session.add(prefecture)
        # 更新の場合
        else:
            prefectureObj.prefecture_id=int(seeder['prefecture_id'])
            prefectureObj.prefecture_name=str(seeder['prefecture_name'])

    db_session.commit()

if __name__ == '__main__':
    seeder_prefectures()
    # seeder_difficulty()
    # seeder_effectiveness()
    seeder_events()
    seeder_types()
    seeder_purposes()
    seeder_parts()
    seeder_trainings()
