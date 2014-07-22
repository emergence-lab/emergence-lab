from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import afm
from .forms import afm_form


class AFMDetail(DetailView):
    """
    Detail view of the afm model.
    """
    model = afm
    template_name = 'afm/afm_detail.html'


class AFMCreate(CreateView):
    """
    View for creation of new afm data.
    """
    model = afm
    template_name = 'afm/afm_create.html'
    form_class = afm_form


class AFMUpdate(UpdateView):
    """
    View for updating afm data.
    """
    model = afm
    template_name = 'afm/afm_update.html'
    form_class = afm_form

    def get_initial(self):
        return {'growth': self.object.growth, 'sample': self.object.sample }
