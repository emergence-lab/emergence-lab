# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from rest_framework import serializers

from .models import SEMScan


class FilePathField(serializers.FileField):
    type_name = "FilePathField"
    widget = forms.TextInput

    def __init__(self, *args, **kwargs):
        kwargs['required'] = False
        kwargs['allow_empty_file'] = True
        super(FilePathField, self).__init__(*args, **kwargs)

    def from_native(self, data):
        return data


class SEMSerializer(serializers.ModelSerializer):
    """
    Serializes the sem model.

    """
    height = FilePathField(max_length=150)
    amplitude = FilePathField(max_length=150)

    class Meta:
        model = SEMScan
        fields = ('uuid', 'image_number', 'magnification', 'source',
                  'image')
