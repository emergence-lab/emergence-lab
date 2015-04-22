# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from braces.views import LoginRequiredMixin
from django_filters.views import FilterView

from core.filters import SampleFilterSet
from core.forms import SampleMultiForm
from core.models import Sample
from core.views import ActionReloadView, PrintTemplate


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


class SampleSplitView(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        piece = self.kwargs.get('piece')
        self.sample = Sample.objects.get_by_uuid(self.kwargs.get('uuid'))

        comment = request.POST.get('split_comment_{}'.format(piece))
        if comment == '':
            comment = None
        num_pieces = int(request.POST.get('split_number_{}'.format(piece)))
        if num_pieces < 2:
            raise ValueError(
                'Invalid number of pieces specified ({}), '
                'must be more than 2'.format(num_pieces))
        self.sample.split(number=num_pieces,
                          piece=piece,
                          comment=comment,
                          user=self.request.user)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('sample_detail', args=(self.sample.uuid,))


class SampleSearchView(LoginRequiredMixin, FilterView):
    template_name = 'core/sample_search.html'
    model = Sample
    filterset_class = SampleFilterSet


class ExportSampleDetail(PrintTemplate):
    template_name = 'core/sample_print.html'

    def get_context_data(self, **kwargs):
        context = super(ExportSampleDetail, self).get_context_data(**kwargs)
        sample = Sample.objects.get(id=Sample.strip_uuid(self.kwargs.get('uuid', None)))
        context['sample'] = sample
        return context
