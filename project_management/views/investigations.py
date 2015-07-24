# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic

from braces.views import LoginRequiredMixin

from core.views import ActiveListView
from core.models import Investigation, Milestone, ProjectTracking
from project_management.forms import InvestigationForm, MilestoneForm


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

    def get_context_data(self, **kwargs):
        context = super(InvestigationDetailView, self).get_context_data(**kwargs)
        investigation = context['investigation']
        context['literature'] = investigation.literature.all()[:20]
        context['processes'] = investigation.target_actions.all().order_by('-timestamp')[:20]
        context['milestones'] = Milestone.objects.filter(
            user=self.request.user).order_by('due_date')
        context['milestone_form'] = MilestoneForm()
        context['active_milestones'] = context['milestones'].filter(is_active=True)
        context['inactive_milestones'] = context['milestones'].filter(is_active=False)
        return context


class InvestigationCreateView(LoginRequiredMixin, generic.CreateView):

    model = Investigation
    template_name = 'project_management/investigation_create.html'
    form_class = InvestigationForm

    def get_form_kwargs(self):
        kwargs = super(InvestigationCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('pm_investigation_detail', kwargs={'slug': self.object.slug})


class InvestigationUpdateView(LoginRequiredMixin, generic.UpdateView):

    model = Investigation
    template_name = 'project_management/investigation_create.html'
    form_class = InvestigationForm

    def get_form_kwargs(self):
        kwargs = super(InvestigationUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('pm_investigation_detail', kwargs={'slug': self.object.slug})
