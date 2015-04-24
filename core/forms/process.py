# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import string

from django import forms

from core.models import DataFile, Process, ProcessTemplate


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


class ProcessCreateForm(AutoCreateForm):

    class Meta:
        model = Process
        fields = ('comment',)


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
