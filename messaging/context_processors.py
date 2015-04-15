# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from .redis_config import Helper


def notifications(request):
    """
    Add notifications to context for all views.
    """
    helper = Helper()
    notification_objects = helper.get_notifications(request.user.id)
    return {'notifications': notification_objects}
