from __future__ import unicode_literals

import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.settings import api_settings

from messaging.redis_config import Helper


class NotificationCreateAPI(APIView):

    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        r = request.POST.get('_content')
        r = json.loads(r)
        h = Helper()
        try:
            notification = h.new_notification(int(r['target']),
                               r['payload'],
                               r['app'],
                               r['url'],
                               r['severity'],
                               int(r['expiration']))

        except Exception as e: raise e
        return Response('Created notification!')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
