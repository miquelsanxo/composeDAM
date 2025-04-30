from utils.db import db
from models.base_model import BaseModel

class CompanyUser(BaseModel):
    __tablename__ = 'company_users'
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    company = db.relationship('Company', backref='company_users')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='company_users')