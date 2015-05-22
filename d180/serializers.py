# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from .models import D180Growth, D180Readings


class D180GrowthSerializer(serializers.ModelSerializer):
    """
    Serializes the growth model.
    """

    class Meta:
        model = D180Growth
        fields = ('id', 'uuid', 'created', 'modified', 'user',
                  'investigations', 'platter', 'comment',
                  'has_gan', 'has_aln', 'has_inn', 'has_algan',
                  'has_ingan', 'other_material', 'orientation',
                  'is_template', 'is_buffer', 'has_pulsed',
                  'has_superlattice', 'has_mqw', 'has_graded',
                  'has_n', 'has_p', 'has_u', 'legacy_identifier',)


class D180ReadingsSerializer(serializers.ModelSerializer):
    """
    Serializes the readings model.
    """
    growth_id = serializers.IntegerField()

    class Meta:
        model = D180Readings
        fields = ('id', 'growth_id', 'layer', 'description', 'pyro_out', 'pyro_in',
                  'tc_in', 'tc_out', 'motor_rpm', 'gc_pressure', 'gc_position',
                  'voltage_in', 'current_in', 'voltage_out', 'current_out',
                  'top_vp_flow', 'hydride_inner', 'hydride_outer',
                  'alkyl_flow_inner', 'alkyl_push_inner', 'alkyl_flow_middle',
                  'alkyl_push_middle', 'alkyl_flow_outer', 'alkyl_push_outer',
                  'n2_flow', 'h2_flow', 'nh3_flow', 'hydride_pressure',
                  'tmga1_flow', 'tmga1_pressure', 'tmga2_flow',
                  'tmga2_pressure', 'tega2_flow', 'tega2_pressure',
                  'tmin1_flow', 'tmin1_pressure', 'tmal1_flow',
                  'tmal1_pressure', 'cp2mg_flow', 'cp2mg_pressure',
                  'cp2mg_dilution', 'silane_flow', 'silane_dilution',
                  'silane_mix', 'silane_pressure', 'ecp_temp')
