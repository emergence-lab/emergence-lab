from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from schedule_queue.models import Reservation
from django.views.generic import ListView, RedirectView
from django.views.generic.edit import CreateView, UpdateView
from django import forms
from django.contrib.auth.models import User
from django.db import models
import time

from schedule_queue import config as tools
import dashboard.urls


class ReservationLanding(ListView):
    model = Reservation
    queryset = tools.get_tool_list()
    template_name = 'schedule_queue/reservation_landing.html'

    def index(request):
        return HttpResponse(queryset)

class ReservationListByTool(ListView):
    model = Reservation
    template_name = 'schedule_queue/reservation_list.html'

    def get_queryset(self):
        tool_slug = self.kwargs['tool_slug']
        return Reservation.objects.exclude(is_active=False).filter(tool=tool_slug).order_by('priority_field')

    def get_context_data(self, **kwargs):
        tool_slug = self.kwargs['tool_slug']
        if 'max_reservations' not in kwargs:
            kwargs['max_reservations'] = tools.get_tool_info(tool_slug)['max_reservations']
        if 'tool_name' not in kwargs:
            kwargs['tool_name'] = tool_slug
        return super(ReservationListByTool, self).get_context_data(**kwargs)

    def index(request):
        return HttpResponse(queryset)

class ReservationCreate(CreateView):
    model = Reservation
    fields = ['tool', 'platter', 'growth_length_in_hours', 'comment', 'bake_length_in_minutes']
    template_name = 'schedule_queue/reservation_form.html'

    #def get_initial(self):
    #    self.object.user = self.request.user

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.priority_field = int(10*time.time())
        self.object.user = self.request.user

        if len(Reservation.objects.exclude(is_active=False).filter(tool=self.object.tool)) < tools.get_tool_info(self.object.tool)['max_reservations'] :
            self.object.save()
            return HttpResponseRedirect(reverse('reservation_list_by_tool', args=(self.object.tool,)))
        else:
            raise Exception("Reservation List Full")

class ReservationEdit(UpdateView):
    model = Reservation
    fields = ['tool', 'platter', 'growth_length_in_hours', 'comment', 'bake_length_in_minutes']
    template_name = 'schedule_queue/reservation_edit.html'

    def get_success_url(self):
        return reverse('reservation_list_by_tool', args=(self.object.tool,))

class IncreasePriority(RedirectView):
    permanent = False
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        reservation_obj = Reservation.objects.get(pk=pk)
        tmp = Reservation.objects.filter(is_active=True, priority_field__lt=reservation_obj.priority_field).order_by('-priority_field')
        if tmp.first():
            tmp = tmp.first()
            reservation_obj.priority_field, tmp.priority_field = tmp.priority_field, reservation_obj.priority_field
            reservation_obj.save()
            tmp.save()
        return reverse('reservation_list_by_tool', args=(reservation_obj.tool,))

class DecreasePriority(RedirectView):
    permanent = False
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        reservation_obj = Reservation.objects.get(pk=pk)
        tmp = Reservation.objects.filter(is_active=True, priority_field__gt=reservation_obj.priority_field).order_by('priority_field')
        if tmp.first():
            tmp = tmp.first()
            reservation_obj.priority_field, tmp.priority_field = tmp.priority_field, reservation_obj.priority_field
            reservation_obj.save()
            tmp.save()
        return reverse('reservation_list_by_tool', args=(reservation_obj.tool,))

class CancelReservation(RedirectView):
    permanent = False
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        reservation_obj = Reservation.objects.get(pk=pk)
        if reservation_obj.is_active and reservation_obj.user == self.request.user:
            reservation_obj.is_active = False
            reservation_obj.save()
        return reverse('reservation_list_by_tool', args=(reservation_obj.tool,))

class CloseReservation(RedirectView):
    permanent = False
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        reservation_obj = Reservation.objects.get(pk=pk)
        if reservation_obj.is_active and reservation_obj.user == self.request.user:
            reservation_obj.is_active = False
            reservation_obj.save()
        return reverse('dashboard')
