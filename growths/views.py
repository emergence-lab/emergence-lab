from django.shortcuts import render
from django.views.generic import DetailView, ListView

from core.models import afm, growth

class growth_list(ListView):
    model = growth
    # cascading search location for template
    # model-appname = app where model is defined
    # view-appname = app where view is defined
    #  1: model-appname/templates/<path>
    #  2: model-appname/templates/model-appname/<default_name>
    template_name = 'core/growth_list.html'

    def get_queryset(self):
        queryset = super(growth_list, self).get_queryset()

        q = self.request.GET.get('q')  # 'q' passed via GET
        if q:
            return queryset.filter(operator__icontains=q)

        return queryset


class growth_detail(DetailView):
    model = growth
    template_name = 'core/growth_detail.html'
    slug_field = 'growth_number'

class afm_detail(DetailView):
    model = afm
    template_name = 'core/afm_detail.html'
