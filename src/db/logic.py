import datetime

from db.schemes import Photo, User


def update_user(user: User, is_activity: bool = True):
    utc_now = datetime.datetime.utcnow()
    user.updated_at = utc_now
    if is_activity:
        user.last_activity_at = utc_now
    user.save()


def update_photo(photo: Photo):
    utc_now = datetime.datetime.utcnow()
    photo.updated_at = utc_now
    photo.save()


def get_user_photos(user_id: int, input_text: str | None = None) -> list[Photo]:
    return Photo.objects(owner_id=user_id, deleted=False).order_by("-created_at")
