from utils.db import db
from models.base_model import BaseModel

class Post(BaseModel):
    __tablename__ = 'posts'
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='posts')
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(255), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    company = db.relationship('Company', backref='posts')
    specialization_id = db.Column(db.Integer, db.ForeignKey('specializations.id'), nullable=True)
    specialization = db.relationship('Specialization', backref='posts')