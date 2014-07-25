from rest_framework import generics, permissions

from .models import afm
from .serializers import AFMSerializer


class AFMListAPI(generics.ListAPIView):
    """
    List all afm scans or create a new one via api.
    """
    queryset = afm.objects.all()
    serializer_class = AFMSerializer
    permission_classes = (permissions.IsAuthenticated, )


class AFMDetailAPI(generics.RetrieveUpdateAPIView):
    """
    Show details or update an afm scan.
    """
    queryset = afm.objects.all()
    serializer_class = AFMSerializer
    permission_classes = (permissions.IsAuthenticated, )


class AFMDestroyAPI(generics.DestroyAPIView):
    """
    Remove an afm scan
    """
    queryset = afm.objects.all()
    serializer_class = AFMSerializer
    permission_classes = (permissions.IsAdminUser, )
