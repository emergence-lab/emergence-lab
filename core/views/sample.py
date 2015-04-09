# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from braces.views import LoginRequiredMixin
from django_filters.views import FilterView

from core.models import Sample
from core.forms import SampleMultiForm
from core.filters import SampleFilterSet


class SampleListView(LoginRequiredMixin, generic.ListView):
    template_name = 'core/sample_list.html'
    model = Sample
    queryset = Sample.objects.order_by('-created')
    paginate_by = 25


class SampleDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'core/sample_detail.html'
    model = Sample
    lookup_url_kwarg = 'uuid'

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        try:
            obj = Sample.objects.get_by_uuid(self.kwargs[self.lookup_url_kwarg])
        except queryset.model.DoesNotExist:
            raise Http404(_('No {}s found matching the query'.format(
                queryset.model._meta.verbose_name)))
        return obj


class SampleCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'core/sample_create.html'
    model = Sample
    form_class = SampleMultiForm

    def form_valid(self, form):
        substrate = form['substrate'].save()
        comment = form['sample'].cleaned_data.get('comment', '')
        sample = Sample.objects.create(substrate, comment)
        return HttpResponseRedirect(
            reverse('sample_detail', kwargs={'uuid': sample.uuid}))


class SampleUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'core/sample_edit.html'
    model = Sample
    lookup_url_kwarg = 'uuid'
    fields = ('comment',)

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        try:
            obj = Sample.objects.get_by_uuid(self.kwargs[self.lookup_url_kwarg])
        except queryset.model.DoesNotExist:
            raise Http404(_('No {}s found matching the query'.format(
                queryset.model._meta.verbose_name)))
        return obj

    def get_success_url(self):
        return reverse('sample_detail', args=(self.object.uuid,))


class SampleSearchView(LoginRequiredMixin, FilterView):
    template_name = 'core/sample_search.html'
    model = Sample
    filterset_class = SampleFilterSet
