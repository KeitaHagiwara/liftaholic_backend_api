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
    db_session.commit()

# 動機、目的、ゴール
def seeder_purposes():
    seeder_json = load_seeder_json('./seeder/purpose.json')
    for seeder in seeder_json:
        purpose = mPurposes(
            purpose_no=int(seeder['purpose_no']),
            purpose_name=str(seeder['purpose_name']),
            purpose_comment=str(seeder['purpose_comment'])
        )
        db_session.add(purpose)
    db_session.commit()

# 部位
def seeder_parts():
    seeder_json = load_seeder_json('./seeder/part.json')
    for seeder in seeder_json:
        part = mParts(
            part_no=int(seeder['part_no']),
            part_name=str(seeder['part_name']),
            sub_part_name=str(seeder['sub_part_name']),
            part_comment=str(seeder['part_comment'])
        )
        db_session.add(part)
    db_session.commit()

# タイプ
def seeder_types():
    seeder_json = load_seeder_json('./seeder/type.json')
    for seeder in seeder_json:
        type = mTypes(
            type_no=int(seeder['type_no']),
            type_name=str(seeder['type_name']),
            type_comment=str(seeder['type_comment'])
        )
        db_session.add(type)
    db_session.commit()

# 種目
def seeder_events():
    seeder_json = load_seeder_json('./seeder/event.json')
    for seeder in seeder_json:
        event = mEvents(
            event_no=int(seeder['event_no']),
            event_name=str(seeder['event_name']),
            event_comment=str(seeder['event_comment'])
        )
        db_session.add(event)
    db_session.commit()

# # 難易度
# def seeder_difficulty():
#     seeder_json = load_seeder_json('./seeder/difficulty.json')
#     for seeder in seeder_json:
#         difficulty = mDifficulty(
#             difficulty_no=int(seeder['difficulty_no']),
#             difficulty_rank=int(seeder['difficulty_rank']),
#             difficulty_name=str(seeder['difficulty_name'])
#         )
#         db_session.add(difficulty)
#     db_session.commit()

# # 効果性
# def seeder_effectiveness():
#     seeder_json = load_seeder_json('./seeder/effectiveness.json')
#     for seeder in seeder_json:
#         effectiveness = mEffectiveness(
#             effectiveness_no=int(seeder['effectiveness_no']),
#             effectiveness_rank=int(seeder['effectiveness_rank']),
#             effectiveness_name=str(seeder['effectiveness_name'])
#         )
#         db_session.add(effectiveness)
#     db_session.commit()

# 都道府県
def seeder_prefectures():
    seeder_json = load_seeder_json('./seeder/prefectures.json')
    for seeder in seeder_json:
        prefecture = mPrefectures(
            prefecture_id=int(seeder['prefecture_id']),
            prefecture_name=str(seeder['prefecture_name'])
        )
        db_session.add(prefecture)
    db_session.commit()

if __name__ == '__main__':
    # seeder_prefectures()
    # seeder_difficulty()
    # seeder_effectiveness()

    # seeder_events()
    # seeder_types()
    # seeder_purposes()
    # seeder_parts()
    seeder_trainings()
