from utils.firebase_utils import get_user_by_token
from models.like import Like
import services.post_service as post_service
import services.like_service as like_service
from utils.exceptions import InternalServerError, ModelNotFoundException, UnauthorizedException, FirebaseException
from utils.utils import make_error_response

def like_post(post_id: int):
    try:
        user = get_user_by_token()
        post = post_service.get_post_by_id(post_id)
        
        like = like_service.get_user_post_like(user.id, post.id)
        
        if like:
            return like_service.delete_like(like.id), 204
        else:
            like = Like(
                user_id=user.id,
                post_id=post.id
            )
            return like_service.add_like(like).serialize(), 201
        
    except (ModelNotFoundException, UnauthorizedException, FirebaseException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
def post_likes(post_id: int):
    try:
        post = post_service.get_post_by_id(post_id)
        likes = like_service.get_post_likes(post.id)
        return len(likes), 200
    except (ModelNotFoundException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))