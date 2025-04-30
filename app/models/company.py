from utils.db import db
from models.base_model import BaseModel

class Company(BaseModel):
    __tablename__ = 'companies'
    name = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=False)