from django import forms

from rest_framework import serializers

from .models import growth, readings


class GrowthSerializer(serializers.ModelSerializer):
    """
    Serializes the growth model.
    """
    growth = serializers.CharField(max_length=50)

    def transform_growth(self, obj, value):
        return value

    def validate_growth(self, attrs, source):
        try:
            growth = growths.models.growth.get_growth(attrs[source])
        except Exception as e:
            raise serializers.ValidationError(str(e))

        attrs[source] = growth
        return attrs

    class Meta:
        model = growth
        fields = ('id', 'growth_number', 'date', 'operator', 'project',
                  'investigation', 'platter', 'reactor', 'run_comments')

class ReadingsSerializer(serializers.ModelSerializer):
    """
    Serializes the readings model.
    """
    growthid = serializers.IntegerField()

    class Meta:
        model = readings
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
