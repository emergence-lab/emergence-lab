# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from rest_framework import serializers

from core.serializers import DataFileSerializer

from .models import AFMScan


class FilePathField(serializers.FileField):
    type_name = "FilePathField"
    widget = forms.TextInput

    def __init__(self, *args, **kwargs):
        kwargs['required'] = False
        kwargs['allow_empty_file'] = True
        super(FilePathField, self).__init__(*args, **kwargs)

    def from_native(self, data):
        return data


class AFMSerializer(serializers.ModelSerializer):
    """
    Serializes the afm model.

    """
    datafiles = DataFileSerializer(many=True, read_only=True)

    class Meta:
        model = AFMScan
        fields = ('uuid', 'created', 'modified', 'datafiles',)
