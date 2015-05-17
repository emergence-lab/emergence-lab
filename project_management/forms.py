# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from datetimewidget.widgets import DateWidget

from .models import Milestone


class MilestoneCreateForm(forms.ModelForm):

    due_date = forms.DateField(widget=DateWidget(
        attrs={'class': 'datetime'},
        bootstrap_version=3,
        options={'minView': '2',
                'startView': '2',
                'todayBtn': 'false',
                'todayHighlight': 'true',
                'clear_Btn': 'true',
                'format': 'yyyy-mm-dd'}
    ))

    class Meta:
        model = Milestone
