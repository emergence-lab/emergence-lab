import django_filters

from .models import Simulation


class SimFilter(django_filters.FilterSet):
    """
    Filter AFM scans on growth (growth number), sample (growth, pocket, piece),
    scan number and location.
    """
    completed = django_filters.BooleanFilter(name='Simulation__completed')
    job = django_filters.NumberFilter(name='Simulation__id')
    node = django_filters.CharFilter(name='Simulation__execution_node')

    class Meta:
        model = Simulation
        fields = ('id', 'user', 'request_date', 'start_date', 'finish_date',
                  'priority', 'execution_node')