# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from datetimewidget.widgets import DateWidget

from core.models import Investigation, Project, Milestone, Task, MilestoneNote


class MilestoneForm(forms.ModelForm):

    class Meta:
        model = Milestone
        fields = ('name', 'due_date', 'description', 'investigation')
        widgets = {
            'investigation': forms.HiddenInput(),
            'due_date': DateWidget(attrs={'class': 'datetime'},
                                   bootstrap_version=3,
                                   usel10n=True,
                                   options={'todayBtn': 'false',
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
                                   options={'todayBtn': 'false',
                                            'todayHighlight': 'true',
                                            'clear_Btn': 'true',
                                            'format': 'yyyy-mm-dd'}),
            'description': forms.Textarea(attrs={'class': 'hallo'}),
        }


class InvestigationForm(forms.ModelForm):

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
        widgets = {
            'description': forms.Textarea(attrs={'class': 'hallo'}),
            'project': forms.HiddenInput(),
        }


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('due_date', 'description',)
        widgets = {
            'due_date': DateWidget(attrs={'class': 'datetime'},
                                   bootstrap_version=3,
                                   usel10n=True,
                                   options={'todayBtn': 'false',
                                            'todayHighlight': 'true',
                                            'clear_Btn': 'true',
                                            'format': 'yyyy-mm-dd'}),
        }


class MilestoneNoteForm(forms.ModelForm):

    class Meta:
        model = MilestoneNote
        fields = ('note',)
        widgets = {
            'note': forms.Textarea(attrs={'class': 'hallo'}),
        }


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description',)
        widgets = {
            'description': forms.Textarea(attrs={'class': 'hallo'}),
        }
