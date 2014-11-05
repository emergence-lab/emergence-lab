from rest_framework import generics, permissions

from .filters import growth_filter
from .models import growth, readings
from .serializers import GrowthSerializer, ReadingsSerializer


class GrowthListAPI(generics.ListCreateAPIView):
    """
    List all growths or create a new one via api.
    """
    queryset = growth.objects.all()
    serializer_class = GrowthSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_class = growth_filter


class GrowthDetailAPI(generics.RetrieveUpdateAPIView):
    """
    Show details or update a growth.
    """
    queryset = growth.objects.all()
    serializer_class = GrowthSerializer
    permission_classes = (permissions.IsAuthenticated, )

class ReadingsListAPI(generics.ListCreateAPIView):
    """
    List all growths or create a new one via api.
    """
    queryset = readings.objects.all()
    serializer_class = ReadingsSerializer
    permission_classes = (permissions.IsAuthenticated, )
    #filter_class = growth_filter


class ReadingsDetailAPI(generics.RetrieveUpdateAPIView):
    """
    Show details or update a growth.
    """
    queryset = readings.objects.all()
    serializer_class = ReadingsSerializer
    permission_classes = (permissions.IsAuthenticated, )