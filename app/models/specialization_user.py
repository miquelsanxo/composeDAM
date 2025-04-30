from utils.db import db
from models.base_model import BaseModel

class SpecializationUser(BaseModel):
    __tablename__ = 'specialization_users'
    specialization_id = db.Column(db.Integer, db.ForeignKey('specializations.id'), nullable=False)
    specialization = db.relationship('Specialization', backref='specialization_users')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='specialization_users')