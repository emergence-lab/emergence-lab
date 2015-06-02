# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic

from braces.views import LoginRequiredMixin

from project_management.models import Milestone
from project_management.forms import MilestoneCreateForm


class MilestoneListView(LoginRequiredMixin, generic.ListView):

    model = Milestone
    template_name = 'project_management/milestone_list.html'

    def get_queryset(self):
        queryset = super(MilestoneListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class MilestoneCreateView(LoginRequiredMixin, generic.CreateView):

    model = Milestone
    template_name = 'project_management/milestone_create.html'
    fields = '__all__'
    form_class = MilestoneCreateForm

    def get_success_url(self):
        return reverse('milestone_list')


class MilestoneDetailView(LoginRequiredMixin, generic.DetailView):

    model = Milestone
    template_name = 'project_management/milestone_detail.html'
