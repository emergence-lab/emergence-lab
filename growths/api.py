from rest_framework import generics, permissions

from .filters import growth_filter
from .models import growth, readings
from .serializers import GrowthSerializer, ReadingsSerializer

#class MultipleFieldLookupMixin(object):
#    """
#    Apply this mixin to any view or viewset to get multiple field filtering
#    based on a `lookup_fields` attribute, instead of the default single field filtering.
#    """
#    def get_object(self):
#        queryset = self.get_queryset()             # Get the base queryset
#        queryset = self.filter_queryset(queryset)  # Apply any filter backends
#        filter = {}
#        for field in self.lookup_fields:
#            filter[field] = self.kwargs[field]
#        return get_object_or_404(queryset, **filter)  # Lookup the object
    
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
    
class GrowthFetchObjectAPI(generics.ListAPIView):
    """
    Show details or update a growth.
    """
    def get_queryset(self):
        growth_number = self.kwargs['growth_number']
        return growth.objects.filter(growth_number=growth_number)
        
    # queryset = growth.objects.all()
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
    
class ReadingsCreateAPI(generics.CreateAPIView):
    """
    List all growths or create a new one via api.
    """
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