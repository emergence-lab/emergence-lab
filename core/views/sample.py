# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from django_filters.views import FilterView

from core.filters import SampleFilterSet
from core.forms import SampleMultiForm
from core.models import Sample, ProcessNode
from core.views import ActionReloadView


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


class SampleAdminView(LoginRequiredMixin, SuperuserRequiredMixin, generic.DetailView):
    template_name = 'core/sample_admin.html'
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


class SampleAdminNodeUpView(LoginRequiredMixin, SuperuserRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        self.sample = Sample.objects.get_by_uuid(self.kwargs.get('uuid'))
        node = self.sample.get_node(self.kwargs.get('node_uuid'))

        if not node.parent.process:  # parent is root node
            print('Not swapping, {} is root'.format(node.process))
            return
        target = node.parent
        while target.process is not None and target.process.type_id == 'split-process':
            target = target.parent

        node.swap_processes(target)
        print('Swapping up {} with {}'.format(node.process, target.process))

    def get_redirect_url(self, *args, **kwargs):
        return reverse('sample_admin', args=(self.sample.uuid,))


class SampleAdminNodeDownView(LoginRequiredMixin, SuperuserRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        self.sample = Sample.objects.get_by_uuid(self.kwargs.get('uuid'))
        node = self.sample.get_node(self.kwargs.get('node_uuid'))

        if node.is_leaf_node():
            print('Not swapping, {} is leaf'.format(node.process))
            return

        qs = (ProcessNode.objects.filter(tree_id=node.tree_id,
                                             level__gt=node.level)
                                      .exclude(process__type_id='split-process')
                                      .order_by('level', 'piece'))
        target = qs.filter(piece=node.piece).first()
        if not target:
            target = qs.first()

        if not target:
            print('Not swapping, {} has no matching node'.format(node.process))

        node.swap_processes(target)
        print('Swapping down {} with {}'.format(node.process, target.process))

    def get_redirect_url(self, *args, **kwargs):
        return reverse('sample_admin', args=(self.sample.uuid,))


class SampleAdminNodeSwapPieceView(LoginRequiredMixin, SuperuserRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        self.sample = Sample.objects.get_by_uuid(self.kwargs.get('uuid'))
        node = self.sample.get_node(self.kwargs.get('node_uuid'))

        piece = request.POST.get('swap_piece')
        if piece == node.piece:
            print('Swapping {} with self'.format(node.process))
            return

        if piece not in self.sample.pieces:
            raise ValueError(
                'Invalid piece ({}), '
                'must be one of {}'.format(piece, self.sample.pieces))

        target = self.sample.leaf_nodes.filter(piece=piece).first()

        node.move_to(target)
        node.piece = piece
        node.save()
        print('Moving {} as child of {}'.format(node.process, target.process))

    def get_redirect_url(self, *args, **kwargs):
        return reverse('sample_admin', args=(self.sample.uuid,))


class SampleAdminNodeSwapSampleView(LoginRequiredMixin, SuperuserRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        self.sample = Sample.objects.get_by_uuid(self.kwargs.get('uuid'))
        node = self.sample.get_node(self.kwargs.get('node_uuid'))

        self.target_sample = Sample.objects.get_by_uuid(request.POST.get('swap_sample'))
        target = self.target_sample.leaf_nodes.first()

        if self.sample.uuid == self.target_sample.uuid:
            print('Swapping {} with self'.format(node.process))
            return

        node.move_to(target)
        node.piece = target.piece
        node.save()
        print('Moving {} as child of {} on sample {}'.format(
            node.process, target.process, self.target_sample))

    def get_redirect_url(self, *args, **kwargs):
        return reverse('sample_admin', args=(self.target_sample.uuid,))


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
