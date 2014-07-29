import django_filters

from .models import afm


class AFMFilter(django_filters.FilterSet):
    """
    Filter AFM scans on growth (growth number), sample (growth, pocket, piece),
    scan number and location.
    """
    growth_number = django_filters.CharFilter(name='growth__growth_number')
    pocket = django_filters.NumberFilter(name='sample__pocket')
    piece = django_filters.CharFilter(name='sample__piece')

    class Meta:
        model = afm
        fields = ['growth', 'growth_number', 'sample', 'pocket', 'piece',
                  'scan_number', 'location']
