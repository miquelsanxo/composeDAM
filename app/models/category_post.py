from utils.db import db
from models.base_model import BaseModel

class CategoryPost(BaseModel):
    __tablename__ = 'category_posts'
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', backref='category_posts')
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    post = db.relationship('Post', backref='category_posts')