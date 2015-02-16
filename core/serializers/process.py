# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from .polymorphic import PolymorphicModelSerializer
from core.models import Process, ProcessNode


class ProcessSerializer(PolymorphicModelSerializer):

    class Meta:
        model = Process
        fields = ('uuid_full', 'uuid', 'created', 'modified', 'comment',
                  'is_destructive')


class ProcessNodeSerializer(serializers.ModelSerializer):
    process = ProcessSerializer()
    parent = serializers.CharField()
    children = serializers.ListField(child=serializers.CharField(),
                                     source='get_children')
    sample = serializers.CharField(source='get_sample')

    class Meta:
        model = ProcessNode
        fields = ('uuid_full', 'uuid', 'created', 'modified', 'comment',
                  'sample', 'piece', 'level', 'parent', 'children', 'process')
        depth = 1
