from rest_framework import generics, permissions

from .filters import growth_filter
from .models import Growth, Readings
from .serializers import GrowthSerializer, ReadingsSerializer

    
class GrowthListAPI(generics.ListCreateAPIView):
    """
    List all growths or create a new one via api.
    """
    queryset = Growth.objects.all()
    serializer_class = GrowthSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_class = growth_filter


class GrowthDetailAPI(generics.RetrieveUpdateAPIView):
    """
    Show details or update a growth.
    """
    queryset = Growth.objects.all()
    serializer_class = GrowthSerializer
    permission_classes = (permissions.IsAuthenticated, )


class GrowthFetchObjectAPI(generics.ListAPIView):
    """
    Show ID of a growth.
    """
    def get_queryset(self):
        growth_number = self.kwargs['growth_number']
        return Growth.objects.filter(uid=growth_number)
        
    serializer_class = GrowthSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ReadingsListAPI(generics.ListCreateAPIView):
    """
    List all readings or create a new one via api.
    """
    queryset = Readings.objects.all()
    serializer_class = ReadingsSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ReadingsCreateAPI(generics.CreateAPIView):
    """
    Create a new reading via api.
    """
    serializer_class = ReadingsSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ReadingsDetailAPI(generics.RetrieveUpdateAPIView):
    """
    Show details or update readings.
    """
    queryset = Readings.objects.all()
    serializer_class = ReadingsSerializer
    permission_classes = (permissions.IsAuthenticated, )
