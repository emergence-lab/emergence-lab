# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import time

from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from schedule_queue.models import Reservation
from django.views import generic

from braces.views import LoginRequiredMixin

from core.models import ProcessType
from core.views import ActionReloadView
from schedule_queue import config as tools


class ReservationLanding(LoginRequiredMixin, generic.ListView):
    model = Reservation
    queryset = ProcessType.objects.all()
    template_name = 'schedule_queue/reservation_landing.html'


class ReservationList(LoginRequiredMixin, generic.ListView):
    model = Reservation
    template_name = 'schedule_queue/reservation_list.html'

    def get_queryset(self):
        tool_slug = self.kwargs['tool_slug']
        return Reservation.objects.exclude(is_active=False).filter(
            tool=tool_slug).order_by('priority')

    def get_context_data(self, **kwargs):
        tool_slug = self.kwargs['tool_slug']
        if 'max_reservations' not in kwargs:
            kwargs['max_reservations'] = tools.get_tool_info(tool_slug)['max_reservations']
        if 'tool_name' not in kwargs:
            kwargs['tool_name'] = tool_slug
        return super(ReservationList, self).get_context_data(**kwargs)


class ReservationCreate(LoginRequiredMixin, generic.CreateView):
    model = Reservation
    fields = ['tool', 'platter', 'growth_length', 'comment', 'bake_length']
    template_name = 'schedule_queue/reservation_form.html'

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.priority = int(10 * time.time())
        self.object.user = self.request.user

        num_reservations = (Reservation.active_objects.filter(tool=self.object.tool)
                                                      .count())
        max_reservations = tools.get_tool_info(self.object.tool)['max_reservations']
        if num_reservations < max_reservations:
            self.object.save()
            return HttpResponseRedirect(reverse('reservation_list',
                                                args=(self.object.tool,)))
        else:
            raise Exception("Reservation List Full")


class ReservationEdit(LoginRequiredMixin, generic.UpdateView):
    model = Reservation
    fields = ['tool', 'platter', 'growth_length',
              'bake_length', 'comment']
    template_name = 'schedule_queue/reservation_edit.html'

    def get_success_url(self):
        return reverse('reservation_list', args=(self.object.tool,))


class IncreasePriority(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        reservation_obj = Reservation.objects.get(pk=pk)
        tmp = (Reservation.active_objects.filter(
            priority__lt=reservation_obj.priority)
            .order_by('-priority'))
        if tmp.first():
            tmp = tmp.first()
            reservation_obj.priority, tmp.priority = \
                tmp.priority, reservation_obj.priority
            reservation_obj.save()
            tmp.save()
        self.tool = reservation_obj.tool

    def get_redirect_url(self, *args, **kwargs):
        return reverse('reservation_list', args=(self.tool,))


class DecreasePriority(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        reservation_obj = Reservation.objects.get(pk=pk)
        tmp = (Reservation.active_objects.filter(
            priority__gt=reservation_obj.priority)
            .order_by('priority'))
        if tmp.first():
            tmp = tmp.first()
            reservation_obj.priority, tmp.priority = \
                tmp.priority, reservation_obj.priority
            reservation_obj.save()
            tmp.save()
        self.tool = reservation_obj.tool

    def get_redirect_url(self, *args, **kwargs):
        return reverse('reservation_list', args=(self.tool,))


class CancelReservation(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        reservation_obj = Reservation.objects.get(pk=pk)
        if reservation_obj.is_active and reservation_obj.user == self.request.user:
            reservation_obj.is_active = False
            reservation_obj.save()
        self.tool = reservation_obj.tool

    def get_redirect_url(self, *args, **kwargs):
        return reverse('reservation_list', args=(self.tool,))


class CloseReservation(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        reservation_obj = Reservation.objects.get(pk=pk)
        if reservation_obj.is_active and reservation_obj.user == self.request.user:
            reservation_obj.is_active = False
            reservation_obj.save()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard')
