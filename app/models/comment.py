from utils.db import db
from models.base_model import BaseModel

class Comment(BaseModel):
    __tablename__ = 'comments'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='comments')
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    post = db.relationship('Post', backref='comments')
    comment = db.Column(db.String(255), nullable=False)
    