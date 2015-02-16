# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from core.models import Substrate, Sample
from .process import PolymorphicModelSerializer


class SubstrateSerializer(PolymorphicModelSerializer):

    class Meta:
        model = Substrate
        fields = ('serial', 'created', 'modified', 'comment', 'source')


class SampleSerializer(serializers.ModelSerializer):
    substrate = SubstrateSerializer()
    nodes = serializers.ListField(child=serializers.CharField())
    pieces = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Sample
        fields = ('uuid', 'created', 'modified', 'comment', 'nodes', 'pieces',
                  'substrate')
        depth = 1
