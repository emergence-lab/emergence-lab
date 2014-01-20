from django.shortcuts import render
from django.views.generic import DetailView, ListView, FormView
from django_filters import FilterSet, CharFilter, NumberFilter
from django_filters.views import FilterView
from django.shortcuts import render_to_response

import sys

from core.models import afm, growth


class growth_filter(FilterSet):
    operator = CharFilter(lookup_type='icontains')
    project = CharFilter(lookup_type='icontains')
    afm__rms = NumberFilter(lookup_type='lt', distinct=True)
    afm__zrange = NumberFilter(lookup_type='lt', distinct=True)

    class Meta:
        model = growth
        fields = ['growth_number', 'operator', 'project', 'afm__rms', 'afm__zrange']
        order_by = ['growth_number']


class growth_list(FilterView):
    filterset_class = growth_filter
    template_name = 'core/growth_filter.html'

    def get_context_data(self, **kwargs):
        context = super(growth_list, self).get_context_data(**kwargs)
        rms = self.request.GET.get('afm__rms')
        rms_lt = self.filterset_class().filters['afm__rms'].lookup_type

        zrange = self.request.GET.get('afm__zrange')
        zrange_lt = self.filterset_class().filters['afm__zrange'].lookup_type

        for growth in context['filter']:
            growth.afm_filter = afm.objects.filter(growth=growth.id)
            if rms:
                growth.afm_filter = growth.afm_filter.filter(**{'rms__'+rms_lt:rms})
            if zrange:
                growth.afm_filter = growth.afm_filter.filter(**{'zrange__'+zrange_lt:zrange})
        
        return context


class growth_detail(DetailView):
    model = growth
    template_name = 'core/growth_detail.html'
    slug_field = 'growth_number'


class afm_detail(DetailView):
    model = afm
    template_name = 'core/afm_detail.html'
