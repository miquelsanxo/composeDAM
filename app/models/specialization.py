from utils.db import db
from models.base_model import BaseModel

class Specialization(BaseModel):
    __tablename__ = 'specializations'
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)