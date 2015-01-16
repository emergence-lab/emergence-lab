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
