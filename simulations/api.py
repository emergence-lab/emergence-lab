from rest_framework import generics, permissions

from .filters import SimFilter
from .models import Simulation
from .serializers import SimSerializer


class SimulationListAPI(generics.ListCreateAPIView):
    """
    List all afm scans or create a new one via api.
    """
    queryset = Simulation.objects.all()
    serializer_class = SimSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_class = SimFilter


class SimulationDetailAPI(generics.RetrieveUpdateAPIView):
    """
    Show details or update an afm scan.
    """
    queryset = Simulation.objects.all()
    serializer_class = SimSerializer
    permission_classes = (permissions.IsAuthenticated, )

class SimulationToDoListAPI(generics.ListAPIView):
    """
    Show ID of Simulatios in line.
    """
    def get_queryset(self):
        instance_type = self.kwargs['instance_type']
        tmp = []
        sims_to_do = Simulation.objects.filter(start_date=None).filter(finish_date=None).filter(execution_node=instance_type).order_by('id')
        for sim in sims_to_do:
            tmp.append(sim)
        return tmp

    serializer_class = SimSerializer
    permission_classes = (permissions.IsAuthenticated, )
