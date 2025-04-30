from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import services.image_service as service
from models.image import Image
from utils.exceptions import BadRequestException, ModelNotFoundException
from utils.constants import NO_IMAGE_PROVIDED, INVALID_IMAGE_FORMAT

def save_image(image: FileStorage, filename: str = None) -> Image:
    if not image:
        raise BadRequestException(NO_IMAGE_PROVIDED)
    
    if image.mimetype not in ['image/jpeg', 'image/png', 'image/gif']:
        raise BadRequestException(INVALID_IMAGE_FORMAT)
    
    filename = secure_filename(image.filename) if filename is None else secure_filename(filename)
    mimetype = image.mimetype
    
    img = service.save_image(Image(img=image.read(), name=filename, mimetype=mimetype))
    return img

def get_image(id: int) -> Image:
    image = service.get_image_by_id(id)
    return image

def delete_image(id: int) -> None:
    try:
        image = service.get_image_by_id(id)
    except ModelNotFoundException:
        return None
    return service.delete_image(image)