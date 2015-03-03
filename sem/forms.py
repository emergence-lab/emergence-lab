# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from .models import SEMScan


class DropzoneForm(forms.ModelForm):

    image_source = forms.CharField(required=False)
    image_number = forms.IntegerField(required=False)

    class Meta:
        model = SEMScan
        fields = ('image_source', 'image_number',)
