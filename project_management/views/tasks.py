# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic

from datetime import datetime

from braces.views import LoginRequiredMixin

from core.views import ActionReloadView
from core.models import Task
from project_management.forms import TaskForm


class TaskListView(LoginRequiredMixin, generic.ListView):

    model = Task
    template_name = 'project_management/task_list.html'

    def get_queryset(self):
        queryset = super(TaskListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):

    model = Task
    template_name = 'project_management/task_create.html'
    fields = '__all__'
    form_class = TaskForm

    def get_success_url(self):
        return reverse('pm_task_list')


class TaskCloseView(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs.pop('pk'))
        if task.user == request.user:
            task.deactivate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('task_list')


class TaskReOpenView(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        task = Task.objects.get(slug=kwargs.pop('pk'))
        if task.user == request.user:
            task.activate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('task_list')
