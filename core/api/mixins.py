# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics


class UUIDRetrieveAPIView(generics.RetrieveAPIView):
    """
    Read-only API view that retrieves an object based on the uuid, either
    short or long. Uses the url kwarg of 'uuid'.
    """
    lookup_url_kwarg = 'uuid'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        uuid = self.kwargs[self.lookup_url_kwarg]

        obj = generics.get_object_or_404(queryset, uuid_full__startswith=uuid)

        self.check_object_permissions(self.request, obj)

        return obj
