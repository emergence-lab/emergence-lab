from django.shortcuts import render
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.edit import FormMixin

from core.models import afm, growth
from .forms import afm_search_form


class growth_list(FormMixin, ListView):
    model = growth
    # cascading search location for template
    # model-appname = app where model is defined
    # view-appname = app where view is defined
    #  1: model-appname/templates/<path>
    #  2: model-appname/templates/model-appname/<default_name>
    template_name = 'core/growth_list.html'
    form_class = afm_search_form

    def get_queryset(self):
        queryset = super(growth_list, self).get_queryset()

        operator = self.request.GET.get('operator')
        if operator:
            queryset = queryset.filter(operator__icontains=operator)
        project = self.request.GET.get('project')
        if project:
            queryset = queryset.filter(project__icontains=project)
        growth_number = self.request.GET.get('growth_number')
        if growth_number:
            queryset = queryset.filter(growth_number__icontains=growth_number)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(growth_list, self).get_context_data(**kwargs)
        context['form'] = afm_search_form
        return context


class growth_detail(DetailView):
    model = growth
    template_name = 'core/growth_detail.html'
    slug_field = 'growth_number'


class afm_detail(DetailView):
    model = afm
    template_name = 'core/afm_detail.html'
