from django.shortcuts import render
from django.views.generic import DetailView, ListView, FormView
from django_filters import FilterSet, CharFilter, NumberFilter
from django_filters.views import FilterView
from django.shortcuts import render_to_response

from core.models import afm, growth

class growth_filter(FilterSet):
    operator = CharFilter(lookup_type='icontains')
    project = CharFilter(lookup_type='icontains')
    afm__rms = NumberFilter(lookup_type='lt', distinct=True)
    class Meta:
        model = growth
        fields = ['growth_number', 'operator', 'project', 'afm__rms']
        order_by = ['growth_number']


class growth_list(FilterView):
    filterset_class = growth_filter
    template_name = 'core/growth_filter.html'


class growth_detail(DetailView):
    model = growth
    template_name = 'core/growth_detail.html'
    slug_field = 'growth_number'


class afm_detail(DetailView):
    model = afm
    template_name = 'core/afm_detail.html'
