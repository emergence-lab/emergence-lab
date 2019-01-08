# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
import string

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from crispy_forms import helper, layout

from core.models import DataFile, Process, ProcessTemplate, ProcessType
from core.utils import DateWidget


class DropzoneForm(forms.ModelForm):

    content_type = forms.CharField(required=False)

    class Meta:
        model = DataFile
        fields = ('content_type',)


class ProcessCreateForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        pieces = kwargs.pop('pieces', string.ascii_lowercase)
        process_type = kwargs.pop('process_type', None)
        super(ProcessCreateForm, self).__init__(*args, **kwargs)
        self.fields['run_date'].required = True
        if process_type != 'generic-process':
            self.fields['type'].widget = forms.HiddenInput()
        else:
            self.fields['type'].queryset = ProcessType.objects.exclude(creation_type='custom')

        self.fields['milestones'] = forms.MultipleChoiceField(required=False, choices=[
            ('{} - {}'.format(i.project.name, i.name), [
                (m.id, m.name) for m in i.milestones.order_by('investigation')])
            for i in user.get_investigations('member') if i.milestones.exists()
        ])
        self.fields['investigations'] = forms.MultipleChoiceField(required=False, choices=[
            (p.name, [(i.id, i.name) for i in p.investigations.order_by('project')])
            for p in user.get_projects('member') if p.investigations.exists()
        ])
        self.fields['pieces'] = forms.MultipleChoiceField(
            choices=zip(pieces, pieces), label='Piece(s) to use')
        if len(pieces) == 1:
            self.fields['pieces'].initial = pieces[0]

    def clean_run_date(self):
        run_date = self.cleaned_data['run_date']
        if run_date > datetime.date.today():
            raise ValidationError(_('Run date cannot be in the future'), code='invalid')
        return run_date

    class Meta:
        model = Process
        fields = ('title', 'run_date', 'comment', 'type', 'investigations', 'milestones')
        labels = {
            'title': 'Short Process Description',
            'run_date': 'Process Performed On',
            'comment': 'Additional Process Comments',
            'type': 'Process Type',
            'investigations': 'Investigation(s)',
            'milestones': 'Milestone(s)',
        }
        widgets = {
            'run_date': DateWidget(attrs={'class': 'date'},
                                   bootstrap_version=3,
                                   usel10n=True,
                                   options={'todayBtn': 'true',
                                            'todayHighlight': 'true',
                                            'clear_Btn': 'true',
                                            'format': 'yyyy-mm-dd'}),
        }


class EditProcessTemplateForm(forms.ModelForm):

    name = forms.CharField(required=False)
    comment = forms.CharField(
        label="Process comments",
        required=False,
        widget=forms.Textarea(attrs={'class': 'hallo'})
    )

    class Meta:
        model = ProcessTemplate
        fields = ('name', 'title', 'comment',)


class WizardBasicInfoForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(WizardBasicInfoForm, self).__init__(*args, **kwargs)
        self.fields['run_date'].required = True

        self.fields['milestones'] = forms.MultipleChoiceField(required=False, choices=[
            ('{} - {}'.format(i.project.name, i.name), [(m.id, m.name) for m in i.milestones.all()])
            for i in user.get_investigations('member') if i.milestones.exists()
        ])
        self.fields['investigations'] = forms.MultipleChoiceField(required=False, choices=[
            (p.name, [(i.id, i.name) for i in p.investigations.all()])
            for p in user.get_projects('member') if p.investigations.exists()
        ])
        self.fields['type'].queryset = ProcessType.objects.exclude(creation_type='custom')
        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'
        self.helper.layout = layout.Layout(
            layout.Field('user'),
            layout.Field('type'),
            layout.Field('run_date'),
            layout.Field('title'),
            layout.Field('comment', css_class='hallo'),
            layout.Field('investigations'),
            layout.Field('milestones'),
        )

    def clean_run_date(self):
        run_date = self.cleaned_data['run_date']
        if run_date > datetime.date.today():
            raise ValidationError(_('Run date cannot be in the future'), code='invalid')
        return run_date

    class Meta:
        model = Process
        fields = ('user', 'type', 'run_date', 'title', 'comment', 'investigations', 'milestones')
        labels = {
            'title': _('Short Description'),
            'comment': _('Additional Comments'),
            'run_date': _('Process Run Date'),
            'type': _('Process Type'),
            'user': _('User'),
            'investigations': _('Investigation(s)'),
            'milestones': _('Milestone(s)'),
        }
        widgets = {
            'run_date': DateWidget(attrs={'class': 'date'},
                                   bootstrap_version=3,
                                   usel10n=True,
                                   options={'todayBtn': 'true',
                                            'todayHighlight': 'true',
                                            'clear_Btn': 'true',
                                            'format': 'yyyy-mm-dd'}),
            'title': forms.TextInput(attrs={'placeholder': _('Short process description')})
        }


class ProcessTypeForm(forms.ModelForm):

    type = forms.RegexField(regex=r'[a-z\-]+',
                            label='Unique Identifier',
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Use lowercase letters and hyphens only'}))

    class Meta:
        model = ProcessType
        fields = ('type', 'name', 'full_name', 'description', 'category',
                  'is_destructive', 'scheduling_type', 'creation_type')
        labels = {
            'name': 'Short Name or Abbreviation',
            'full_name': 'Full Name',
            'is_destructive': 'Does this process type alter the sample properties?',
            'creation_type': 'Does this process need custom handling for creation?'
        }
