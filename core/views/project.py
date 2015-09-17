# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic

from braces.views import LoginRequiredMixin

from .utility import ActionReloadView
from core.models import Investigation, Project, ProjectTracking
from core.forms import CreateProjectForm, TrackProjectForm
from .mixins import AccessControlMixin


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    """
    View for creating a project.
    """
    template_name = 'core/project_create.html'
    model = Project
    form_class = CreateProjectForm

    def form_valid(self, form):
        response = super(ProjectCreateView, self).form_valid(form)
        p = ProjectTracking.objects.get_or_create(project=self.object,
                                            user=self.request.user)
        self.request.user.groups.add(p[0].project.owner_group)
        return response

    def get_success_url(self):
        return reverse('pm_project_list')


class TrackProjectRedirectView(LoginRequiredMixin, ActionReloadView):
    """
    Sets the specified project as tracked for the logged in user.
    """

    def perform_action(self, request, *args, **kwargs):
        slug = kwargs.pop('slug')
        project = Project.objects.get(slug=slug)
        user = self.request.user
        ProjectTracking.objects.get_or_create(project=project,
                                              user=user,
                                              defaults={'is_owner': False})

    def get_redirect_url(self, *args, **kwargs):
        return reverse('pm_project_list')


class UntrackProjectRedirectView(LoginRequiredMixin, ActionReloadView):
    """
    Sets the specified project as not tracked for the logged in user.
    """

    def perform_action(self, request, *args, **kwargs):
        slug = kwargs.pop('slug')
        project = Project.objects.get(slug=slug)
        user = self.request.user
        tracking = ProjectTracking.objects.filter(project=project, user=user)
        if tracking.count():
            tracking.delete()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('pm_project_list')


class ActivateProjectRedirectView(AccessControlMixin, ActionReloadView):
    """
    Sets the specified project to active.
    """

    membership = 'owner'

    def get_group_required(self):
        self.project = Project.objects.get(slug=self.kwargs.get('slug'))
        return super(ActivateProjectRedirectView, self).get_group_required(
            self.membership, self.project)

    def perform_action(self, request, *args, **kwargs):
        self.project.activate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('pm_project_detail', args=(self.project.slug,))


class DeactivateProjectRedirectView(AccessControlMixin, ActionReloadView):
    """
    Sets the specified project to inactive.
    """

    membership = 'owner'

    def get_group_required(self):
        self.project = Project.objects.get(slug=self.kwargs.get('slug'))
        return super(DeactivateProjectRedirectView, self).get_group_required(
            self.membership, self.project)

    def perform_action(self, request, *args, **kwargs):
        self.project.deactivate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('pm_project_detail', args=(self.project.slug,))


class ActivateInvestigationRedirectView(AccessControlMixin, ActionReloadView):
    """
    Sets the specified investigation to active.
    """

    membership = 'owner'

    def get_group_required(self):
        self.investigation = Investigation.objects.get(slug=self.kwargs.get('slug'))
        return super(ActivateInvestigationRedirectView, self).get_group_required(
            self.membership, self.investigation)

    def perform_action(self, request, *args, **kwargs):
        self.investigation.activate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('pm_investigation_detail', args=(self.investigation.slug,))


class DeactivateInvestigationRedirectView(AccessControlMixin, ActionReloadView):
    """
    Sets the specified investigation to inactive.
    """

    membership = 'owner'

    def get_group_required(self):
        self.investigation = Investigation.objects.get(slug=self.kwargs.get('slug'))
        return super(DeactivateInvestigationRedirectView, self).get_group_required(
            self.membership, self.investigation)

    def perform_action(self, request, *args, **kwargs):
        self.investigation.deactivate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('pm_investigation_detail', args=(self.investigation.slug,))


class TrackProjectView(LoginRequiredMixin, generic.CreateView):
    """
    View to handle tracking projects.
    """
    model = ProjectTracking
    form_class = TrackProjectForm
    template_name = 'core/track_project.html'

    def form_valid(self, form):
        project_id = form.cleaned_data['project']
        try:
            self.object = ProjectTracking.objects.get(user=self.request.user,
                                                      project_id=project_id)
            self.object.is_owner = form.cleaned_data['is_owner']
            self.object.save()
        except:
            self.object = form.save(user=self.request.user)
        return HttpResponseRedirect(reverse('dashboard'))
