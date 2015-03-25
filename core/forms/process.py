# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from core.models import DataFile


class DropzoneForm(forms.ModelForm):

    content_type = forms.CharField(required=False)

    class Meta:
        model = DataFile
        fields = ('content_type',)
