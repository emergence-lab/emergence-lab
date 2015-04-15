# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from rest_framework import serializers

from core.serializers.process import DataFileSerializer

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
    #image = FilePathField(max_length=150)
    datafiles = DataFileSerializer(many=True, read_only=True)

    class Meta:
        model = SEMScan
        fields = ('uuid', 'created', 'modified',
                  'image_source', 'datafiles')
