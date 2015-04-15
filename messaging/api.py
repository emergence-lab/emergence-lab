# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from messaging.redis_config import Helper


class NotificationCreateAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        content = json.loads(request.POST.get('_content'))
        helper = Helper()
        helper.new_notification(int(content['target']), content['payload'],
                                content['app'], content['url'],
                                content['severity'], int(content['expiration']))
        return Response('Created notification!')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
