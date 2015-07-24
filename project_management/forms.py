# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from datetimewidget.widgets import DateWidget

from core.models import Investigation, ProjectTracking, Project, Milestone, Task, MilestoneNote


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


class MilestoneSimpleForm(forms.ModelForm):

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
        fields = ('due_date', 'name', 'description',)


class InvestigationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(InvestigationForm, self).__init__(*args, **kwargs)
        project_tracking = [x.project_id for x in ProjectTracking.objects.all().filter(user=user)]
        projects = Project.objects.all().filter(id__in=project_tracking)
        self.fields['project'].queryset = projects

    def clean_name(self):
        name = self.cleaned_data['name']
        reserved_names = [
            'activate',
            'deactivate',
            'add-investigation',
            'all',
            'list',
        ]
        if name in reserved_names:
            self.add_error('name',
                'Investigation name "{}" is reserved, please choose another'.format(name))
        return name

    class Meta:
        model = Investigation
        fields = ('name', 'description', 'project',)


class TaskForm(forms.ModelForm):

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
        model = Task
        fields = ('due_date', 'description',)


class MilestoneNoteForm(forms.ModelForm):

    # note = forms.CharField(
    #     widget=forms.Textarea(attrs={'class': 'hallo'}))

    class Meta:
        model = MilestoneNote
        fields = ('note',)
