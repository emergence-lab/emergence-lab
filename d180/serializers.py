# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from core.serializers import ProcessSerializer
from .models import D180Growth, D180Readings


class D180GrowthSerializer(ProcessSerializer):
    """
    Serializes the growth model.
    """

    class Meta:
        model = D180Growth
        fields = ('uuid', 'created', 'modified', 'user',
                  'investigations', 'platter', 'comment')

    has_gan = models.BooleanField(default=False)
    has_aln = models.BooleanField(default=False)
    has_inn = models.BooleanField(default=False)
    has_algan = models.BooleanField(default=False)
    has_ingan = models.BooleanField(default=False)
    other_material = models.CharField(max_length=50, blank=True)

    # layer orientation
    orientation = models.CharField(max_length=10, default='0001')

    # growth features
    is_template = models.BooleanField(default=False)
    is_buffer = models.BooleanField(default=False)
    has_pulsed = models.BooleanField(default=False)
    has_superlattice = models.BooleanField(default=False)
    has_mqw = models.BooleanField(default=False)
    has_graded = models.BooleanField(default=False)

    # doping features
    has_n = models.BooleanField(default=False)
    has_p = models.BooleanField(default=False)
    has_u = models.BooleanField(default=False)

class D180ReadingsSerializer(serializers.ModelSerializer):
    """
    Serializes the readings model.
    """
    growthid = serializers.IntegerField()

    class Meta:
        model = D180Readings
        fields = ('id', 'growth', 'layer', 'layer_desc', 'pyro_out', 'pyro_in',
                  'tc_in', 'tc_out', 'motor_rpm', 'gc_pressure', 'gc_position',
                  'voltage_in', 'current_in', 'voltage_out', 'current_out',
                  'top_vp_flow', 'hydride_inner', 'hydride_outer',
                  'alkyl_flow_inner', 'alkyl_push_inner', 'alkyl_flow_middle',
                  'alkyl_push_middle', 'alkyl_flow_outer',  'alkyl_push_outer',
                  'n2_flow', 'h2_flow', 'nh3_flow', 'hydride_pressure',
                  'tmga1_flow', 'tmga1_pressure', 'tmga2_flow',
                  'tmga2_pressure', 'tega2_flow', 'tega2_pressure',
                  'tmin1_flow', 'tmin1_pressure', 'tmal1_flow',
                  'tmal1_pressure', 'cp2mg_flow', 'cp2mg_pressure',
                  'cp2mg_dilution', 'silane_flow', 'silane_dilution',
                  'silane_mix', 'silane_pressure', 'ecp_temp')
