from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.generic import View, CreateView, ListView, DetailView

from .models import hall
from core.views import SessionHistoryMixin


class hall_list(SessionHistoryMixin, ListView):
    model = hall
    template_name = 'hall/hall_list.html'


class hall_detail(SessionHistoryMixin, DetailView):
    model = hall
    template_name = 'hall/hall_detail.html'
