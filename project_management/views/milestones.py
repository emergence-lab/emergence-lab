# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponseRedirect

from datetime import datetime

from braces.views import LoginRequiredMixin

from core.views import ActionReloadView
from core.models import Milestone, MilestoneNote

from project_management.forms import MilestoneForm


class MilestoneListView(LoginRequiredMixin, generic.ListView):

    model = Milestone
    template_name = 'project_management/milestone_list.html'

    def get_context_data(self, **kwargs):
        context = super(MilestoneListView, self).get_context_data(**kwargs)
        context['today'] = datetime.now()
        return context

    def get_queryset(self):
        queryset = super(MilestoneListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class MilestoneCreateView(LoginRequiredMixin, generic.CreateView):

    model = Milestone
    template_name = 'project_management/milestone_create.html'
    fields = '__all__'
    form_class = MilestoneForm

    def get_success_url(self):
        return reverse('milestone_list')


class MilestoneUpdateView(LoginRequiredMixin, generic.UpdateView):

    model = Milestone
    template_name = 'project_management/milestone_update.html'
    fields = '__all__'
    form_class = MilestoneForm

    def get_success_url(self):
        return reverse('milestone_list')


class MilestoneCloseView(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        slug = kwargs.pop('slug')
        milestone = Milestone.objects.get(slug=slug)
        milestone.deactivate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('milestone_list')


class MilestoneReOpenView(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        slug = kwargs.pop('slug')
        milestone = Milestone.objects.get(slug=slug)
        milestone.activate()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('milestone_list')


class MilestoneDetailView(LoginRequiredMixin, generic.ListView):

    model = MilestoneNote
    template_name = 'project_management/milestone_detail.html'
    paginate_by = 5

    def get_queryset(self):
        milestone = Milestone.objects.get(slug=self.kwargs.get('slug'))
        queryset = MilestoneNote.objects.all().filter(milestone=milestone)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MilestoneDetailView, self).get_context_data(**kwargs)
        context['today'] = datetime.now()
        context['milestone'] = Milestone.objects.get(slug=self.kwargs.get('slug'))
        context['processes'] = context['milestone'].processes.order_by('-created')[:10]
        context['literature'] = context['milestone'].literature.order_by('-created')[:10]
        return context


class MilestoneNoteAction(LoginRequiredMixin, generic.View):

    def post(self, request, *args, **kwargs):
        note = request.POST.get('note')
        slug = request.POST.get('slug')
        #user_id = request.POST.get('user')
        MilestoneNote.objects.create(note=note,
                                        user=request.user,
                                        milestone=Milestone.objects.get(slug=slug))
        return HttpResponseRedirect(reverse('milestone_detail', kwargs={'slug': slug}))
