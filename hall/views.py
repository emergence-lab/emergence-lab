from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.generic import View, CreateView, ListView, DetailView

from .models import hall


class hall_list(ListView):
    model = hall
    template_name = 'hall/hall_list.html'


class hall_detail(DetailView):
    model = hall
    template_name = 'hall/hall_detail.html'
