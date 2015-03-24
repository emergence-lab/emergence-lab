# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from rest_framework import serializers

from .models import Hall


class HallSerializer(serializers.ModelSerializer):
    """
    Serializes the afm model.

    """

    class Meta:
        model = Hall
        fields = ('uuid', 'pk',)
