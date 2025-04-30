from utils.db import db
from models.base_model import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)