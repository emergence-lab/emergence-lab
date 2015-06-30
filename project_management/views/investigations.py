# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic
from django.conf import settings

from braces.views import LoginRequiredMixin

from core.views import ActiveListView
from core.models import Investigation, ProjectTracking
from project_management.forms import InvestigationForm


class InvestigationListView(LoginRequiredMixin, ActiveListView):

    template_name = 'project_management/investigation_list.html'
    model = Investigation

    def get_queryset(self):
        queryset = super(InvestigationListView, self).get_queryset()
        projects = [x.project for x in ProjectTracking.objects.all().filter(user=self.request.user)]
        return queryset.filter(project__in=projects)


class InvestigationDetailView(LoginRequiredMixin, generic.DetailView):

    template_name = 'project_management/investigation_detail.html'
    model = Investigation


class InvestigationCreateView(LoginRequiredMixin, generic.CreateView):

    model = Investigation
    template_name = 'project_management/investigation_create.html'
    form_class = InvestigationForm

    def get_form_kwargs(self):
        kwargs = super(InvestigationCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
