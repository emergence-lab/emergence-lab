from django.shortcuts import render
from django.views.generic import DetailView, ListView

from core.models import afm, growth
from .filters import growth_filter, RelationalFilterView


class growth_list(RelationalFilterView):
    filterset_class = growth_filter
    template_name = 'core/growth_filter.html'


class afm_compare(ListView):
    template_name = 'core/afm_compare.html'

    def get_queryset(self):
        id_list = [int(id) for id in self.request.GET.getlist('afm')]
        objects = afm.objects.filter(id__in=id_list)
        return objects


class growth_detail(DetailView):
    model = growth
    template_name = 'core/growth_detail.html'
    slug_field = 'growth_number'


class afm_detail(DetailView):
    model = afm
    template_name = 'core/afm_detail.html'
