### Classes for Redis objects associated with this app
from django.conf import settings
from django.utils import timezone

from redis import StrictRedis
import uuid
import pickle


class Helper(object):
    """
    Helper functions for the app. UPDATE LATER.
    """
    def __init__(self):
        self.r = StrictRedis(settings.REDIS_HOST,
                             settings.REDIS_PORT,
                             settings.REDIS_DB)

    def get_notifications(self, user_id):
        ### LATER: ADD GROUPS AND LABS
        notifications = []
        notification_set = self.r.lrange(
            'users:{0}:notifications'.format(user_id),
                      0, -1)
        for i in notification_set:
            if self.r.get(i):
                notifications.append(pickle.loads(self.r.get(i)))
            else:
                self.r.lrem('users:{0}:notifications'.format(user_id),
                          0, i)
        return notifications

    def new_notification(self, target, notification, app=None, url=None, severity=None, expiration=30):
        ### LATER: ADD GROUPS AND LABS
        notification_id = str(uuid.uuid4())
        item = Notification()
        item.created = timezone.datetime.now()
        item.payload = notification
        item.app = app
        item.url = url
        if severity not in ['success', 'warning', 'info', 'danger']:
            item.severity = None
        else: item.severity = severity
        self.r.set(notification_id, pickle.dumps(item))
        self.r.expire(notification_id, expiration*24*3600)
        self.r.lpush('users:{0}:notifications'.format(target), notification_id)


class Notification(object):
    """
    Empty class for notification objects.
    """
    def init(self):
        self.created = timezone.datetime.now()
        self.payload = None
        self.severity = None
        self.expiration = 30


