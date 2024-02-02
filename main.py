from fastapi import FastAPI
from config import settings
from api import home, planning, workout, notification, shopping, mypage


app = FastAPI()

# ホーム画面のAPI
app.include_router(home.router)

# プランニング画面のAPI
app.include_router(planning.router)

# ワークアウト画面のAPI
app.include_router(workout.router)

# お知らせ画面のAPI
app.include_router(notification.router)

# ショッピング画面のAPI
app.include_router(shopping.router)

# マイページ画面のAPI
app.include_router(mypage.router)
