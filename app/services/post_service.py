from utils.db import db
from models.post import Post
from utils.exceptions import ModelNotFoundException

def get_all_posts() -> list:
    return Post.query.all()

def add_post(post: Post) -> Post:
    db.session.add(post)
    db.session.commit()
    return post

def get_post_by_id(post_id: int) -> Post:
    post = Post.query.get(post_id)
    if not post:
        raise ModelNotFoundException("Post", post_id)
    return post

def delete_post(post_id: int) -> None:
    post = get_post_by_id(post_id)
    db.session.delete(post)
    db.session.commit()
    
def update_post(post: Post) -> Post:
    old_post = get_post_by_id(post.id)
    
    old_post.title = post.title
    old_post.description = post.description
    old_post.photo = post.photo
    old_post.specialization_id = post.specialization_id
    old_post.price = post.price
    old_post.company_id = post.company_id
    
    db.session.commit()
    return old_post
    