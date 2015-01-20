# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import RedirectView

from braces.views import LoginRequiredMixin

from core.models import User
from .utility import ActiveListView


class UserListView(LoginRequiredMixin, ActiveListView):
    """
    View to list all user and provide actions.
    """
    template_name = "core/operator_list.html"
    model = User


class ActivateUserRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified user to active.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.pop('id')
        user = User.objects.get(pk=pk)
        user.activate()
        return reverse('operator_list')


class DeactivateUserRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified user to inactive.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.pop('id')
        user = User.objects.get(pk=pk)
        user.deactivate()
        return reverse('operator_list')
