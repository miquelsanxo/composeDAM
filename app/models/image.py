from utils.db import db
from models.base_model import BaseModel

class Image(BaseModel):
    __tablename__ = 'image'
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    mimetype = db.Column(db.String(50), nullable=False)