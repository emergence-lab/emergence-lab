# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic

from braces.views import LoginRequiredMixin

from core.views import ActiveListView, AccessControlMixin
from core.models import Investigation, Milestone, ProjectTracking, Project
from project_management.forms import InvestigationForm, MilestoneForm


class InvestigationAccessControlMixin(AccessControlMixin):
    """
    Implements AccessControlMixin for Investigation as kwarg to view.
    """

    def get_group_required(self):
        self.investigation = Investigation.objects.get(slug=self.kwargs.get('slug'))
        return super(InvestigationAccessControlMixin, self).get_group_required(
            self.membership, self.investigation)


class InvestigationListView(LoginRequiredMixin, ActiveListView):

    template_name = 'project_management/investigation_list.html'
    model = Investigation

    def get_queryset(self):
        queryset = super(InvestigationListView, self).get_queryset()
        projects = [x.project for x in ProjectTracking.objects.all().filter(user=self.request.user)]
        return queryset.filter(project__in=projects)


class InvestigationDetailView(InvestigationAccessControlMixin, generic.DetailView):

    template_name = 'project_management/investigation_detail.html'
    model = Investigation

    membership = 'viewer'

    def get_context_data(self, **kwargs):
        context = super(InvestigationDetailView, self).get_context_data(**kwargs)
        investigation = context['investigation']
        context['literature'] = investigation.literature.all()[:20]
        context['processes'] = investigation.target_actions.all().order_by('-timestamp')[:20]
        context['milestones'] = (Milestone.objects.filter(user=self.request.user)
                                                  .filter(investigation=self.object)
                                                  .order_by('due_date'))
        context['milestone_form'] = MilestoneForm(
            initial={
                'investigation': investigation,
            })
        context['active_milestones'] = context['milestones'].filter(is_active=True)
        context['inactive_milestones'] = context['milestones'].filter(is_active=False)
        return context


class InvestigationCreateView(LoginRequiredMixin, generic.CreateView):

    model = Investigation
    template_name = 'project_management/investigation_create.html'
    form_class = InvestigationForm

    def get_initial(self):
        self.project = Project.objects.get(slug=self.kwargs.get('project'))
        initial = super(InvestigationCreateView, self).get_initial()
        initial['project'] = self.project
        return initial

    def post(self, request, *args, **kwargs):
        self.project = Project.objects.get(slug=kwargs.get('project'))
        if self.project.is_owner(self.request.user):
            return super(InvestigationCreateView, self).post(request, *args, **kwargs)
        else:
            self.object = None
            form = self.get_form()
            form.add_error('project',
                'You do not have permission to create an investigation for this project.')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('pm_investigation_detail', kwargs={'slug': self.object.slug})


class InvestigationUpdateView(InvestigationAccessControlMixin, generic.UpdateView):

    model = Investigation
    template_name = 'project_management/investigation_edit.html'
    form_class = InvestigationForm

    membership = 'owner'

    def get_success_url(self):
        return reverse('pm_investigation_detail', kwargs={'slug': self.object.slug})
