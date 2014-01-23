from django.shortcuts import render
from django.views.generic import DetailView

from core.models import afm, growth
from .filters import growth_filter, RelationalFilterView


class growth_list(RelationalFilterView):
    filterset_class = growth_filter
    template_name = 'core/growth_filter.html'


class growth_detail(DetailView):
    model = growth
    template_name = 'core/growth_detail.html'
    slug_field = 'growth_number'


class afm_detail(DetailView):
    model = afm
    template_name = 'core/afm_detail.html'
