# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic

from datetime import datetime

from braces.views import LoginRequiredMixin

from core.views import ActionReloadView
from core.models import Milestone

from project_management.forms import MilestoneForm


class MilestoneListView(LoginRequiredMixin, generic.ListView):

    model = Milestone
    template_name = 'project_management/milestone_list.html'

    def get_context_data(self, **kwargs):
        context = super(MilestoneListView, self).get_context_data(**kwargs)
        context['today'] = datetime.now()
        return context

    def get_queryset(self):
        queryset = super(MilestoneListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class MilestoneCreateView(LoginRequiredMixin, generic.CreateView):

    model = Milestone
    template_name = 'project_management/milestone_create.html'
    fields = '__all__'
    form_class = MilestoneForm

    def get_success_url(self):
        return reverse('milestone_list')


class MilestoneUpdateView(LoginRequiredMixin, generic.UpdateView):

    model = Milestone
    template_name = 'project_management/milestone_update.html'
    fields = '__all__'
    form_class = MilestoneForm

    def get_success_url(self):
        return reverse('milestone_list')


class MilestoneDetailView(LoginRequiredMixin, generic.DetailView):

    model = Milestone
    template_name = 'project_management/milestone_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MilestoneDetailView, self).get_context_data(**kwargs)
        context['today'] = datetime.now()
        return context


class MilestoneCloseView(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        slug = kwargs.pop('slug')
        milestone = Milestone.objects.get(slug=slug)
        milestone.deactivate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('milestone_list')


class MilestoneReOpenView(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        slug = kwargs.pop('slug')
        milestone = Milestone.objects.get(slug=slug)
        milestone.activate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('milestone_list')
