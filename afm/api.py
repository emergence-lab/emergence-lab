from rest_framework import generics, permissions

from .filters import AFMFilter
from .models import afm
from .serializers import AFMSerializer


class AFMListAPI(generics.ListCreateAPIView):
    """
    List all afm scans or create a new one via api.
    """
    queryset = afm.objects.all()
    serializer_class = AFMSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_class = AFMFilter


class AFMDetailAPI(generics.RetrieveUpdateAPIView):
    """
    Show details or update an afm scan.
    """
    queryset = afm.objects.all()
    serializer_class = AFMSerializer
    permission_classes = (permissions.IsAuthenticated, )
