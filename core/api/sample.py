# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics, permissions

from core.models import Sample
from core.serializers import SampleSerializer


class SampleListAPIView(generics.ListAPIView):
    """
    Read-only API view to list details for all samples.
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 100


class SampleRetrieveAPIView(generics.RetrieveAPIView):
    """
    Read-only API view to show shallow details for a sample from the uuid.
    Does not retrieve the entire process tree.
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = 'uuid'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        uuid = Sample.strip_uuid(self.kwargs[self.lookup_url_kwarg])

        obj = generics.get_object_or_404(queryset, id=uuid)

        self.check_object_permissions(self.request, obj)

        return obj
