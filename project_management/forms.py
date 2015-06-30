# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from datetimewidget.widgets import DateWidget

from core.models import Investigation, ProjectTracking, Project, Milestone


class MilestoneForm(forms.ModelForm):

    due_date = forms.DateField(widget=DateWidget(
        attrs={'class': 'datetime'},
        bootstrap_version=3,
        usel10n=True,
        options={'minView': '2',
                'startView': '2',
                'todayBtn': 'false',
                'todayHighlight': 'true',
                'clear_Btn': 'true',
                'format': 'yyyy-mm-dd'}
    ))

    class Meta:
        model = Milestone
        fields = '__all__'


class InvestigationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user=kwargs.pop('user')
        super(InvestigationForm, self).__init__(*args, **kwargs)
        project_tracking = [x.project_id for x in ProjectTracking.objects.all().filter(user=user)]
        projects = Project.objects.all().filter(id__in=project_tracking)
        self.fields['project'].queryset = projects

    class Meta:
        model = Investigation
        fields = ('name', 'description', 'project',)
