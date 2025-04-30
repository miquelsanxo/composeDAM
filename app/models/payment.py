from utils.db import db
from models.base_model import BaseModel

class Payment(BaseModel):
    __tablename__ = 'payments'
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user1 = db.relationship('User', foreign_keys=[user1_id], backref='payments_user1')
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2 = db.relationship('User', foreign_keys=[user2_id], backref='payments_user2')
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    post = db.relationship('Post', backref='payments')
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, server_default=db.func.now())
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'), nullable=False)
    payment_method = db.relationship('PaymentMethod', backref='payments')