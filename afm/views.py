from django.shortcuts import render
from django.views.generic import DetailView
from .models import afm


class afm_detail(DetailView):
    model = afm
    template_name = 'afm/afm_detail.html'
