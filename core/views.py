import os

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, TemplateView

from .models import investigation, operator, platter, project


class SessionHistoryMixin(object):
    max_history = 5
    request = None

    def add_breadcrumb_history(self, request):
        history = request.session.get('breadcrumb_history', [])

        if not history or history[-1] != request.path:
            history.append(request.path)

        if len(history) > self.max_history:
            history.pop(0)

        request.session['breadcrumb_history'] = history
        return history

    def get_context_data(self, **kwargs):
        kwargs['breadcrumb'] = self.add_breadcrumb_history(self.request)
        return super(SessionHistoryMixin, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(SessionHistoryMixin, self).dispatch(request, *args, **kwargs)
        

class ActiveListView(ListView):
    """
    View to handle models using the active and inactive manager.
    """
    def get_context_data(self, **kwargs):
        context = super(ActiveListView, self).get_context_data(**kwargs)
        context['active_list'] = self.model.current.all()
        context['inactive_list'] = self.model.retired.all()
        return context


class homepage(TemplateView):
    """
    View for the homepage of the application.
    """
    template_name = "core/index.html"


def protected_media(request, filename):
    fullpath = os.path.join(settings.MEDIA_ROOT, filename)
    response = HttpResponse(mimetype='image/jpeg')
    response['X-Sendfile'] = fullpath
    return response


class operator_list(ActiveListView):
    """
    View to list all operators and provide actions.
    """
    template_name = "core/operator_list.html"
    model = operator


class operator_create(CreateView):
    """
    View to create operators.
    """
    template_name = "core/operator_create.html"
    model = operator
    fields = ['name']

    def get_success_url(self):
        return reverse('operator_list')


class platter_list(ActiveListView):
    """
    View to list all operators and provide actions.
    """
    template_name = "core/platter_list.html"
    model = platter


class project_list(ActiveListView):
    """
    View to list all projects and provide actions.
    """
    template_name = "core/project_list.html"
    model = project


class investigation_list(ActiveListView):
    """
    View to list all projects and provide actions.
    """
    template_name = "core/investigation_list.html"
    model = investigation
