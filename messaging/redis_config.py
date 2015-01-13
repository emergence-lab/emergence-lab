### Classes for Redis objects associated with this app
from django.conf import settings

from redis import StrictRedis
import uuid

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
                notifications.append(self.r.get(i))
            else:
                self.r.lrem('users:{0}:notifications'.format(user_id),
                          0, i)
        return notifications

    def new_notification(self, target, notification):
        ### LATER: ADD GROUPS AND LABS
        notification_id = str(uuid.uuid4())
        self.r.lpush('users:{0}:notifications'.format(target), notification_id)
        self.r.set(notification_id, notification)


class Notification(object):
    """
    Empty class for notification objects.
    """
    pass

