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

class growth_detail(DetailView):
    model = growth
    template_name = 'core/growth_detail.html'

class afm_detail(DetailView):
    model = afm
    template_name = 'core/afm_detail.html'
