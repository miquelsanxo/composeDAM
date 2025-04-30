from utils.db import db
from models.like import Like
from utils.exceptions import ModelNotFoundException

def get_all_like() -> list:
    return Like.query.all()

def add_like(like: Like) -> Like:
    db.session.add(like)
    db.session.commit()
    return like

def get_like_by_id(like_id: int) -> Like:
    like = Like.query.get(like_id)
    if not like:
        raise ModelNotFoundException("Like", like_id)
    return like

def get_post_likes(post_id: int) -> list:
    return Like.query.filter_by(post_id=post_id).all()

def get_user_post_like(user_id: int, post_id: int) -> Like:
    return Like.query.filter_by(user_id=user_id, post_id=post_id).first()

def delete_like(like_id: int) -> None:
    like = get_like_by_id(like_id)
    db.session.delete(like)
    db.session.commit()
    
def update_like(like: Like) -> Like:
    old_like = get_like_by_id(like.id)
    
    old_like.user_id = like.user_id
    old_like.post_id = like.post_id
    
    db.session.commit()
    return old_like
    