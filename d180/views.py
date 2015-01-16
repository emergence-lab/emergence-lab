# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic

from braces.views import LoginRequiredMixin

from .models import Platter
from core.views import ActionReloadView, ActiveListView


class PlatterListView(LoginRequiredMixin, ActiveListView):
    """
    View to list all operators and provide actions.
    """
    template_name = "growths/platter_list.html"
    model = Platter


class PlatterCreateView(LoginRequiredMixin, generic.CreateView):
    """
    View for creating a platter.
    """
    template_name = 'growths/platter_create.html'
    model = Platter
    fields = ('name', 'serial',)

    def form_valid(self, form):
        form.instance.is_active = True
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('platter_list')


class ActivatePlatterReloadView(LoginRequiredMixin, ActionReloadView):
    """
    Sets the specified platter to active.
    """

    def perform_action(self, request, *args, **kwargs):
        pk = kwargs.pop('id')
        platter = Platter.objects.get(pk=pk)
        platter.activate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('platter_list')


class DeactivatePlatterReloadView(LoginRequiredMixin, ActionReloadView):
    """
    Sets the specified platter to inactive.
    """

    def perform_action(self, request, *args, **kwargs):
        pk = kwargs.pop('id')
        platter = Platter.objects.get(pk=pk)
        platter.deactivate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('platter_list')
