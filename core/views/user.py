# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse

from braces.views import LoginRequiredMixin

from core.models import User
from .utility import ActiveListView, ActionReloadView


class UserListView(LoginRequiredMixin, ActiveListView):
    """
    View to list all user and provide actions.
    """
    template_name = "core/operator_list.html"
    model = User


class ActivateUserRedirectView(LoginRequiredMixin, ActionReloadView):
    """
    Sets the specified user to active.
    """

    def perform_action(self, request, *args, **kwargs):
        pk = kwargs.pop('id')
        user = User.objects.get(pk=pk)
        user.activate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('operator_list')


class DeactivateUserRedirectView(LoginRequiredMixin, ActionReloadView):
    """
    Sets the specified user to inactive.
    """

    def perform_action(self, request, *args, **kwargs):
        pk = kwargs.pop('id')
        user = User.objects.get(pk=pk)
        user.deactivate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('operator_list')
