# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from core.models import Substrate, Sample
from .process import ProcessRootNodeSerializer


class SubstrateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Substrate
        fields = ('serial', 'created', 'modified', 'comment', 'source')


class SampleSerializer(serializers.ModelSerializer):
    substrate = SubstrateSerializer()
    process_tree = ProcessRootNodeSerializer()

    class Meta:
        model = Sample
        fields = ('uuid', 'created', 'modified', 'comment',
                  'substrate', 'process_tree')
        depth = 1
