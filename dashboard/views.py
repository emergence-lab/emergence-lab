# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pickle
import uuid

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView

from braces.views import LoginRequiredMixin
from redis import StrictRedis

from core.models import User, Project, Investigation, ProcessType
from core.streams import project_stream, investigation_stream
from core.views import ActionReloadView
from users.redis_config import ActionItem


class DashboardMixin(object):
    """
    Mixin that populates the context with active and inactive projects,
    as well as user-context items.
    """
    def get_context_data(self, **kwargs):
        projects = (User.objects.filter(pk=self.request.user.id)
                                .values_list('projects__id', flat=True))
        kwargs['active_projects'] = Project.active_objects.filter(id__in=projects)
        kwargs['inactive_projects'] = Project.inactive_objects.filter(id__in=projects)

        kwargs['reservations'] = []
        r = StrictRedis(settings.REDIS_HOST,
                        settings.REDIS_PORT,
                        settings.REDIS_DB)
        kwargs['action_items'] = []
        for i in r.lrange('users:{0}:action.items'.format(self.request.user.id),
                          0, -1):
            kwargs['action_items'].append(pickle.loads(i))
        return super(DashboardMixin, self).get_context_data(**kwargs)


class Dashboard(LoginRequiredMixin, DashboardMixin, DetailView):
    """
    Main dashboard for the user with commonly used actions.
    """
    template_name = 'dashboard/dashboard.html'
    model = User
    object = None

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['growths'] = []
        context['tools'] = ProcessType.objects.values_list('name', flat=True)
        return context

    def get_object(self, queryset=None):
        return self.object


class ProjectDetailDashboardView(LoginRequiredMixin, DashboardMixin, DetailView):
    """
    View for details of a project in the dashboard.
    """
    template_name = 'dashboard/project_detail_dashboard.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailDashboardView, self).get_context_data(**kwargs)
        context['stream'] = project_stream(self.object)
        return context


class InvestigationDetailDashboardView(LoginRequiredMixin, DashboardMixin, DetailView):
    """
    View for details of an investigation in the dashboard.
    """
    template_name = 'dashboard/investigation_detail_dashboard.html'
    model = Investigation

    def get_context_data(self, **kwargs):
        context = super(InvestigationDetailDashboardView, self).get_context_data(**kwargs)
        context['project'] = self.object.project
        context['stream'] = investigation_stream(self.object)
        return context


class AddActionItemView(LoginRequiredMixin, DashboardMixin, ActionReloadView):
    """
    View for adding action item via Redis
    """

    def perform_action(self, request, *args, **kwargs):
        action_item = ActionItem()
        action_item.comment = str(self.request.POST.get('comment'))
        r = StrictRedis(settings.REDIS_HOST,
                        settings.REDIS_PORT,
                        settings.REDIS_DB)
        if self.request.POST.get('update_field'):
            index = self.request.POST.get('update_field')
            original = pickle.loads(
                r.lindex('users:{}:action.items'.format(self.request.user.id),
                         index))
            original.comment = action_item.comment
            r.lset('users:{}:action.items'.format(self.request.user.id),
                   index, pickle.dumps(original))
        else:
            action_item.created = timezone.datetime.now()
            r.lpush('users:{}:action.items'.format(self.request.user.id),
                    pickle.dumps(action_item))

    def get_redirect_url(self, *args, **kwargs):
        return str(reverse('dashboard') + "#action_items")


class RemoveActionItemView(LoginRequiredMixin, DashboardMixin, ActionReloadView):
    """
    View for adding action item via Redis
    """

    def perform_action(self, request, *args, **kwargs):
        r = StrictRedis(settings.REDIS_HOST,
                        settings.REDIS_PORT,
                        settings.REDIS_DB)
        index = kwargs['action_item']
        tmp = uuid.uuid4().hex
        r.lset('users:{0}:action.items'.format(self.request.user.id), index, tmp)
        r.lrem('users:{0}:action.items'.format(self.request.user.id), 0, tmp)

    def get_redirect_url(self, *args, **kwargs):
        return str(reverse('dashboard') + "#action_items")
