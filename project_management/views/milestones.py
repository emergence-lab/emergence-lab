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

    def get_context_data(self, **kwargs):
        context = super(MilestoneDetailView, self).get_context_data(**kwargs)
        updates = [x for x in ProgressUpdate.objects.all().filter(milestone=self.object)]
        context['progress'] = updates
        return context
