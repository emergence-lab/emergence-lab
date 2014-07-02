from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView

import growths.models
import afm.models
from .filters import growth_filter, RelationalFilterView


class growth_list(RelationalFilterView):
    filterset_class = growth_filter
    template_name = 'growths/growth_filter.html'


class afm_compare(ListView):
    template_name = 'growths/afm_compare.html'

    def get_queryset(self):
        id_list = [int(id) for id in self.request.GET.getlist('afm')]
        objects = afm.models.afm.objects.filter(id__in=id_list)
        return objects


class growth_detail(DetailView):
    model = growths.models.growth
    template_name = 'growths/growth_detail.html'
    slug_field = 'growth_number'


class create_growth(CreateView):
    model = growths.models.growth
    template_name = 'growths/create_growth.html'

    def get_success_url(self):
        return reverse('home')
