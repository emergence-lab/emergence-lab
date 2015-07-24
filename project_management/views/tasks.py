# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponseRedirect

from datetime import datetime

from braces.views import LoginRequiredMixin

from core.views import ActionReloadView
from core.models import Task, Milestone
from project_management.forms import TaskForm


class TaskListView(LoginRequiredMixin, generic.ListView):

    model = Task
    template_name = 'project_management/task_list.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['today'] = datetime.now()
        context['inactive_tasks'] = Task.objects.all().filter(
            user=self.request.user).filter(is_active=False).order_by("due_date")
        return context

    def get_queryset(self):
        queryset = super(TaskListView, self).get_queryset().filter(user=self.request.user)
        return queryset.filter(is_active=True).order_by("due_date")


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
        return reverse('milestone_detail', kwargs={'slug': kwargs.pop('slug')})


class TaskReOpenView(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs.pop('pk'))
        if task.user == request.user:
            task.activate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('milestone_detail', kwargs={'slug': kwargs.pop('slug')})


class TaskCreateAction(LoginRequiredMixin, generic.View):

    def post(self, request, *args, **kwargs):
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            self.object = task_form.save(commit=False)
            self.object.user = request.user
            self.object.save()
        milestone = Milestone.objects.get(id=request.POST.get('milestone'))
        return HttpResponseRedirect(reverse('milestone_detail', kwargs={'slug': milestone.slug}))
