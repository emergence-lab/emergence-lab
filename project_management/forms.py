# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from datetimewidget.widgets import DateWidget

from core.models import Investigation, ProjectTracking, Project, Milestone, Task, MilestoneNote


class MilestoneForm(forms.ModelForm):

    class Meta:
        model = Milestone
        fields = ('name', 'due_date', 'description', 'user', 'investigation')
        widgets = {
            'investigation': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'due_date': DateWidget(attrs={'class': 'datetime'},
                                   bootstrap_version=3,
                                   usel10n=True,
                                   options={'minView': '2',
                                            'startView': '2',
                                            'todayBtn': 'false',
                                            'todayHighlight': 'true',
                                            'clear_Btn': 'true',
                                            'format': 'yyyy-mm-dd'}),
            'description': forms.Textarea(attrs={'class': 'hallo'}),
        }


class MilestoneSimpleForm(forms.ModelForm):

    class Meta:
        model = Milestone
        fields = ('due_date', 'name', 'description',)
        widgets = {
            'due_date': DateWidget(attrs={'class': 'datetime'},
                                   bootstrap_version=3,
                                   usel10n=True,
                                   options={'minView': '2',
                                            'startView': '2',
                                            'todayBtn': 'false',
                                            'todayHighlight': 'true',
                                            'clear_Btn': 'true',
                                            'format': 'yyyy-mm-dd'}),
            'description': forms.Textarea(attrs={'class': 'hallo'}),
        }


class InvestigationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(InvestigationForm, self).__init__(*args, **kwargs)
        project_tracking = (ProjectTracking.objects.filter(user=user)
                                                   .values_list('project_id', flat=True))
        projects = Project.objects.filter(id__in=project_tracking)
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

    class Meta:
        model = Task
        fields = ('due_date', 'description',)
        widgets = {
            'due_date': DateWidget(attrs={'class': 'datetime'},
                                   bootstrap_version=3,
                                   usel10n=True,
                                   options={'minView': '2',
                                            'startView': '2',
                                            'todayBtn': 'false',
                                            'todayHighlight': 'true',
                                            'clear_Btn': 'true',
                                            'format': 'yyyy-mm-dd'}),
        }


class MilestoneNoteForm(forms.ModelForm):

    class Meta:
        model = MilestoneNote
        fields = ('note',)
