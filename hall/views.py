# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.views import generic

from .models import Hall


class HallListView(generic.ListView):
    model = Hall
    template_name = 'hall/hall_list.html'


class HallDetailView(generic.DetailView):
    model = Hall
    template_name = 'hall/hall_detail.html'

    def get_context_data(self, **kwargs):
        context = super(HallDetailView, self).get_context_data(**kwargs)
        process = Hall.objects.get(id=self.kwargs['pk'])
        context['process_id'] = process.id
        context['dataset'] = [i.halldata for i in process.datafiles.get_queryset()]
        return context
