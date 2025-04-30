from utils.db import db
from models.base_model import BaseModel

class User(BaseModel):
    __tablename__ = 'users'
    uid = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    full_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    birth_date = db.Column(db.Date, nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(255), nullable=True)