from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView

from .models import afm
from .forms import afm_form


class afm_detail(DetailView):
    """
    Detail view of the afm model.
    """
    model = afm
    template_name = 'afm/afm_detail.html'


class afm_create(CreateView):
    """
    View for creation of new afm data.
    """
    model = afm
    template_name = 'afm/afm_create.html'
    form_class = afm_form
