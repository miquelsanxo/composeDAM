import os
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone

load_dotenv()

DEBUG = os.getenv("DEBUG", "False") == "True"

DATABASE_CONNECTION_URI = os.getenv("DATABASE_CONNECTION_URI", "sqlite:///database.db")

TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Madrid")

PORT = os.getenv("PORT", 8000)

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "admin")

FIREBASECONFIG = {
    "apiKey": "AIzaSyDxLBYdHFUZp4JIwgoCWpEJgz9C8d5SLvA",
    "authDomain": "connectyourcoach-98301.firebaseapp.com",
    "projectId": "connectyourcoach-98301",
    "storageBucket": "connectyourcoach-98301.firebasestorage.app",
    "messagingSenderId": "509247796997",
    "appId": "1:509247796997:web:5abaa6ccb8a2acbbbee96c",
    "databaseURL": "https://connectyourcoach-98301.firebaseio.com",
    "measurementId": "G-GWGP24YMY7"
}

def date_now() -> datetime:
    return datetime.now(timezone(TIME_ZONE)).replace(tzinfo=None)