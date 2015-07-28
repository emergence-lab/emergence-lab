# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import string

from django import forms

from crispy_forms import helper, layout

from core.models import (DataFile, Process, ProcessTemplate, Milestone,
                         ProjectTracking, Investigation)


class DropzoneForm(forms.ModelForm):

    content_type = forms.CharField(required=False)

    class Meta:
        model = DataFile
        fields = ('content_type',)


class AutoCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        pieces = kwargs.pop('pieces', string.ascii_lowercase)

        super(AutoCreateForm, self).__init__(*args, **kwargs)

        self.fields['pieces'] = forms.MultipleChoiceField(
            choices=zip(pieces, pieces), label='Piece(s) to use')

    class Meta:
        model = Process
        fields = ('comment', 'type')


ProcessCreateForm = AutoCreateForm


class EditProcessTemplateForm(forms.ModelForm):

    name = forms.CharField(required=False)
    comment = forms.CharField(
        label="Process comments",
        required=False,
        widget=forms.Textarea(attrs={'class': 'hallo'})
    )

    class Meta:
        model = ProcessTemplate
        fields = ('name', 'comment',)


class WizardBasicInfoForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(WizardBasicInfoForm, self).__init__(*args, **kwargs)
        self.fields['investigations'].required = False
        projs = (ProjectTracking.objects.filter(user=user)
                                        .values_list('project_id', flat=True))
        self.fields['investigations'].queryset = Investigation.objects.filter(project_id__in=projs)
        self.fields['milestones'].required = False
        self.fields['milestones'].queryset = Milestone.objects.filter(user=user)
        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'
        self.helper.layout = layout.Layout(
            layout.Field('user'),
            layout.Field('type'),
            layout.Field('comment', css_class='hallo'),
            layout.Field('investigations'),
            layout.Field('milestones'),
        )

    class Meta:
        model = Process
        fields = ('user', 'type', 'comment', 'investigations', 'milestones')
        labels = {
            'comment': 'Process Comments',
            'type': 'Process Type',
            'user': 'User',
            'investigations': 'Investigation(s)',
            'milestones': 'Milestone(s)',
        }
