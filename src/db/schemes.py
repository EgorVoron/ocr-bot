import datetime

from mongoengine import (BooleanField, DateTimeField, Document, IntField,
                         StringField)

from bot import limits
from utils import today_min_datetime


class User(Document):  # legacy
    # default
    user_id = IntField(required=True, unique=True)  # equivalent to LongField
    first_name = StringField()
    last_name = StringField()
    username = StringField()
    language_code = StringField()
    is_blocked = BooleanField(default=False)
    is_deactivated = BooleanField(default=False)

    # datetime
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
    last_activity_at = DateTimeField(default=datetime.datetime.utcnow)

    # promotion
    is_promoted = BooleanField(default=False)
    promoted_at = DateTimeField()
    promoted_until = DateTimeField()
    alerted_on_promotion_end = BooleanField(default=False)

    # stats
    total_searches = IntField(default=0)
    total_deletions = IntField(default=0)

    meta = {"indexes": ["user_id"]}

    def today_savings(self) -> int:
        return Photo.objects(
            owner_id=self.user_id, created_at__gte=today_min_datetime()
        ).count()

    def still_promoted(self) -> bool:
        if not self.is_promoted:
            return False
        utc_now = datetime.datetime.utcnow()
        if utc_now > self.promoted_until:
            self.is_promoted = False
            self.updated_at = utc_now
            self.save()
            return self.is_promoted
        return True

    def reached_limit(self) -> bool:
        return self.today_savings() >= limits.MAX_PHOTOS_PER_DAY


class Photo(Document):
    file_id = StringField(required=True)
    file_unique_id = StringField(required=True)
    result_id = StringField(required=True)
    owner_id = IntField(required=True)
    text_lat = StringField()
    text_cyr = StringField()

    """
    priority:
    0 - premium
    1-2 - priority of updating
    """
    priority = IntField(required=True)
    times_sent = IntField(default=0)
    deleted = BooleanField(default=False)
    text_is_correct = BooleanField(default=False)

    """
    statuses: 
    0 - no update (deprecated)
    1 - needs to be updated by updater, 
    2 - update in progress, 
    3 - updated
    """
    status = IntField(min_value=0, default=1)
    update_started_at = DateTimeField()

    # datetime
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {"indexes": ["owner_id", "created_at"]}


class TransferCode(Document):
    from_id = IntField(required=True)
    value = StringField(required=True)
