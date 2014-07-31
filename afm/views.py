from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import afm
from .forms import afm_form
from core.views import SessionHistoryMixin


class AFMList(SessionHistoryMixin, ListView):
    """
    List the most recent afm data
    """
    model = afm
    template_name = 'afm/afm_list.html'
    paginate_by = 25


class AFMDetail(SessionHistoryMixin, DetailView):
    """
    Detail view of the afm model.
    """
    model = afm
    template_name = 'afm/afm_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AFMDetail, self).get_context_data(**kwargs)
        context['sample_siblings'] = [a for a in afm.objects.filter(sample=self.get_object().sample).exclude(id=self.get_object().id).order_by('location', 'scan_number')]
        context['pocket_siblings'] = [a for a in afm.objects.filter(growth=self.get_object().growth, sample__pocket=self.get_object().sample.pocket).exclude(id=self.get_object().id).exclude(sample=self.get_object().sample).order_by('sample__piece', 'location', 'scan_number')]
        context['growth_siblings'] = [a for a in afm.objects.filter(growth=self.get_object().growth).exclude(sample__pocket=self.get_object().sample.pocket).exclude(sample=self.get_object().sample).order_by('sample').order_by('sample__growth', 'sample__piece', 'location', 'scan_number')]
        return context


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


class AFMDelete(DeleteView):
    """
    View for deleting afm data
    """
    model = afm
    template_name = 'afm/afm_delete.html'

    def get_success_url(self):
        return reverse('afm_list')
