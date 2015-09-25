# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponseRedirect

from datetime import datetime

from braces.views import LoginRequiredMixin

from core.views import ActionReloadView, AccessControlMixin
from core.models import Milestone, MilestoneNote, Investigation

from project_management.forms import MilestoneForm, TaskForm, MilestoneNoteForm


class MilestoneAccessControlMixin(AccessControlMixin):
    """
    Implements AccessControlMixin for Milestone as kwarg to view.
    """

    def get_group_required(self):
        self.milestone = Milestone.objects.get(slug=self.kwargs.get('slug'))
        return super(MilestoneAccessControlMixin, self).get_group_required(
            self.membership, self.milestone)


class MilestoneListView(LoginRequiredMixin, generic.ListView):

    model = Milestone
    template_name = 'project_management/milestone_list.html'

    def get_context_data(self, **kwargs):
        context = super(MilestoneListView, self).get_context_data(**kwargs)
        context['today'] = datetime.now()
        return context

    def get_queryset(self):
        queryset = super(MilestoneListView, self).get_queryset()
        return [x for x in queryset if x.is_viewer(self.request.user)]


class MilestoneCreateView(LoginRequiredMixin, generic.CreateView):

    model = Milestone
    template_name = 'project_management/milestone_create.html'
    form_class = MilestoneForm

    def get_initial(self):
        self.investigation = Investigation.objects.get(slug=self.kwargs.get('investigation'))
        initial = super(MilestoneCreateView, self).get_initial()
        initial['investigation'] = self.investigation
        initial['user'] = self.request.user
        return initial

    def post(self, request, *args, **kwargs):
        self.investigation = Investigation.objects.get(slug=kwargs.get('investigation'))
        if self.investigation.is_owner(self.request.user):
            return super(MilestoneCreateView, self).post(request, *args, **kwargs)
        else:
            self.object = None
            form = self.get_form()
            form.add_error('investigation',
                'You do not have permission to create a milestone for this investigation.')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('milestone_detail', kwargs={'slug': self.object.slug})


class MilestoneUpdateView(MilestoneAccessControlMixin, generic.UpdateView):

    model = Milestone
    template_name = 'project_management/milestone_update.html'
    form_class = MilestoneForm

    membership = 'owner'

    def get_success_url(self):
        return reverse('milestone_detail', kwargs={'slug': self.object.slug})


class MilestoneCloseView(MilestoneAccessControlMixin, ActionReloadView):

    membership = 'owner'

    def perform_action(self, request, *args, **kwargs):
        self.slug = kwargs.pop('slug')
        milestone = Milestone.objects.get(slug=self.slug)
        milestone.deactivate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('milestone_detail', kwargs={'slug': self.slug})


class MilestoneReOpenView(MilestoneAccessControlMixin, ActionReloadView):

    membership = 'owner'

    def perform_action(self, request, *args, **kwargs):
        self.slug = kwargs.pop('slug')
        milestone = Milestone.objects.get(slug=self.slug)
        milestone.activate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('milestone_detail', kwargs={'slug': self.slug})


class MilestoneDetailView(MilestoneAccessControlMixin, generic.ListView):

    model = MilestoneNote
    template_name = 'project_management/milestone_detail.html'
    paginate_by = 10

    membership = 'viewer'

    def get_queryset(self):
        queryset = MilestoneNote.objects.all().filter(
            milestone=self.milestone).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MilestoneDetailView, self).get_context_data(**kwargs)
        tasks = self.milestone.task.filter(user=self.request.user).order_by('due_date')
        context['today'] = datetime.now()
        context['milestone'] = self.milestone
        context['processes'] = self.milestone.processes.order_by('-created')[:20]
        context['literature'] = self.milestone.literature.order_by('-created')[:20]
        context['active_tasks'] = tasks.filter(is_active=True)[:20]
        context['inactive_tasks'] = tasks.filter(is_active=False)[:20]
        context['note_form'] = MilestoneNoteForm()
        context['task_form'] = TaskForm()
        return context


class MilestoneNoteAction(LoginRequiredMixin, generic.View):

    def post(self, request, *args, **kwargs):
        note_form = MilestoneNoteForm(request.POST)
        milestone = Milestone.objects.get(id=request.POST.get('milestone'))
        if note_form.is_valid() and milestone.is_member(self.request.user):
            self.object = note_form.save(commit=False)
            self.object.milestone_id = milestone.id
            self.object.user_id = request.POST.get('user')
            self.object.save()
        else:
            HttpResponseRedirect(reverse('milestone_detail', kwargs={'slug': milestone.slug}))
        return HttpResponseRedirect(reverse('milestone_detail', kwargs={'slug': milestone.slug}))
