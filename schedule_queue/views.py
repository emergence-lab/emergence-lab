# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import time

from django.db.models import Count
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from schedule_queue.models import Reservation
from django.views import generic

from braces.views import LoginRequiredMixin

from core.models import ProcessType
from core.views import ActionReloadView
from d180.models import Platter


class ReservationLanding(LoginRequiredMixin, generic.ListView):
    model = Reservation
    queryset = (ProcessType.objects
                           .filter(configuration__core_scheduling_type='simple')
                           .filter(reservation__is_active=True)
                           .annotate(open_reservations=Count('reservation')))
    template_name = 'schedule_queue/reservation_landing.html'


class ReservationList(LoginRequiredMixin, generic.ListView):
    model = Reservation
    template_name = 'schedule_queue/reservation_list.html'

    def get_queryset(self):
        process_type = self.kwargs.get('process')
        return (Reservation.active_objects.filter(tool_id=process_type)
                           .order_by('priority'))

    def get_context_data(self, **kwargs):
        process_type = ProcessType.objects.get(type=self.kwargs.get('process'))
        if 'max_reservations' not in kwargs:
            kwargs['max_reservations'] = 8
        if 'tool_name' not in kwargs:
            kwargs['process_type'] = process_type
        return super(ReservationList, self).get_context_data(**kwargs)


class ReservationCreate(LoginRequiredMixin, generic.CreateView):
    model = Reservation
    fields = ['tool', 'platter', 'growth_length', 'comment', 'bake_length']
    template_name = 'schedule_queue/reservation_form.html'

    def get_form(self, form_class=None):
        form = super(ReservationCreate, self).get_form(form_class)
        form.fields['platter'].queryset = Platter.active_objects.all()
        return form

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.priority = int(10 * time.time())
        self.object.user = self.request.user

        num_reservations = (Reservation.active_objects.filter(tool=self.object.tool)
                                                      .count())
        max_reservations = 8
        if num_reservations < max_reservations:
            self.object.save()
            return HttpResponseRedirect(reverse('reservation_list',
                                                args=(self.object.tool_id,)))
        else:
            raise Exception("Reservation List Full")


class ReservationEdit(LoginRequiredMixin, generic.UpdateView):
    model = Reservation
    fields = ['tool', 'platter', 'growth_length',
              'bake_length', 'comment']
    template_name = 'schedule_queue/reservation_edit.html'

    def get_success_url(self):
        return reverse('reservation_list', args=(self.object.tool_id,))


class IncreasePriority(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(pk=self.kwargs.get('pk'))
        reservation.increase_priority(save=True)
        self.process_type = reservation.tool_id

    def get_redirect_url(self, *args, **kwargs):
        return reverse('reservation_list', args=(self.process_type,))


class DecreasePriority(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(pk=self.kwargs.get('pk'))
        reservation.decrease_priority(save=True)
        self.process_type = reservation.tool_id

    def get_redirect_url(self, *args, **kwargs):
        return reverse('reservation_list', args=(self.process_type,))


class CancelReservation(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(pk=self.kwargs.get('pk'))
        if reservation.user_id == self.request.user.id:
            reservation.deactivate(save=True)
        self.process_type = reservation.tool_id

    def get_redirect_url(self, *args, **kwargs):
        return reverse('reservation_list', args=(self.process_type,))


class CloseReservation(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(pk=self.kwargs.get('pk'))
        if reservation.user_id == self.request.user.id:
            reservation.deactivate(save=True)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard')
