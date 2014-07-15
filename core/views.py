from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .models import operator


class homepage(TemplateView):
    """
    View for the homepage of the application.
    """
    template_name = "core/index.html"


class operator_list(ListView):
    """
    View to list all operators and provide actions.
    """
    template_name = "core/operator_list.html"
    model = operator

    def get_context_data(self, **kwargs):
        context = super(operator_list, self).get_context_data(**kwargs)
        context['active_list'] = operator.current.all()
        context['inactive_list'] = operator.retired.all()
        return context