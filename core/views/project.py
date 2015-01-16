# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import (CreateView, DetailView, RedirectView,
                                  UpdateView)

from braces.views import LoginRequiredMixin

from .misc import ActiveListView
from core.models import Investigation, Project, ProjectTracking, User
from core.forms import TrackProjectForm
from core.streams import project_stream, investigation_stream


class ProjectListView(LoginRequiredMixin, ActiveListView):
    """
    View to list all projects and provide actions.
    """
    template_name = "core/project_list.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['tracking'] = (ProjectTracking.objects.filter(user=self.request.user)
                                                      .values_list('project_id', flat=True))
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """
    View for details of a project.
    """
    template_name = 'core/project_detail.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        if 'username' in self.kwargs:
            userid = User.objects.filter(username=self.kwargs['username']).values('id')
            context['tracking'] = (ProjectTracking.objects.filter(user_id=userid,
                                                                  project=self.object)
                                                          .exists())
        else:
            context['tracking'] = (ProjectTracking.objects.filter(user=self.request.user,
                                                                  project=self.object)
                                                          .exists())
        context['growths'] = []
        context['entries'] = []
        context['stream'] = project_stream(self.object)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a project.
    """
    template_name = 'core/project_create.html'
    model = Project
    fields = ('name', 'description',)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('project_detail_all', kwargs={'slug': self.object.slug})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for editing information about a project.
    """
    template_name = 'core/project_update.html'
    model = Project
    fields = ('description',)

    def get_success_url(self):
        return reverse('project_detail_all', kwargs={'slug': self.object.slug})


class TrackProjectRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified project as tracked for the logged in user.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.pop('slug')
        project = Project.objects.get(slug=slug)
        user = self.request.user
        ProjectTracking.objects.get_or_create(project=project,
                                              user=user,
                                              defaults={'is_owner': False})
        return reverse('project_list')


class UntrackProjectRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified project as not tracked for the logged in user.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.pop('slug')
        project = Project.objects.get(slug=slug)
        user = self.request.user
        tracking = ProjectTracking.objects.filter(project=project, user=user)
        if tracking.count():
            tracking.delete()
        return reverse('project_list')


class ActivateProjectRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified project to active.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.pop('slug')
        project = Project.objects.get(slug=slug)
        project.activate()
        return reverse('project_list')


class DeactivateProjectRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified project to inactive.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.pop('slug')
        project = Project.objects.get(slug=slug)
        project.deactivate()
        return reverse('project_list')


class InvestigationDetailView(LoginRequiredMixin, DetailView):
    """
    View for details of an investigation.
    """
    template_name = 'core/investigation_detail.html'
    model = Investigation

    def get_context_data(self, **kwargs):
        context = super(InvestigationDetailView, self).get_context_data(**kwargs)
        context['stream'] = investigation_stream(self.object)
        context['project'] = self.object.project
        context['growths'] = []
        context['entries'] = []
        return context


class InvestigationCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating an investigation.
    """
    template_name = 'core/investigation_create.html'
    model = Investigation
    fields = ('name', 'description')

    def dispatch(self, request, *args, **kwargs):
        self.initial = {'project': Project.objects.get(slug=kwargs.pop('slug'))}
        return super(InvestigationCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.project = self.initial['project']
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('investigation_detail_all', kwargs={'project': self.object.project.slug,
                                                           'slug': self.object.slug})


class InvestigationUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for editing information about a project.
    """
    template_name = 'core/investigation_update.html'
    model = Investigation
    fields = ('description',)

    def get_success_url(self):
        return reverse('investigation_detail_all', kwargs={'project': self.object.project.slug,
                                                           'slug': self.object.slug})


class InvestigationListView(LoginRequiredMixin, ActiveListView):
    """
    View to list all projects and provide actions.
    """
    template_name = "core/investigation_list.html"
    model = Investigation


class ActivateInvestigationRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified investigation to active.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.pop('slug')
        investigation = Investigation.objects.get(slug=slug)
        investigation.activate()
        return reverse('project_list')


class DeactivateInvestigationRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified investigation to inactive.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.pop('slug')
        investigation = Investigation.objects.get(slug=slug)
        investigation.deactivate()
        return reverse('project_list')


class TrackProjectView(LoginRequiredMixin, CreateView):
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
