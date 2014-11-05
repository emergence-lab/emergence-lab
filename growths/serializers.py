from django import forms
from rest_framework import serializers

from .models import growth, readings
#import growths.models


#class FilePathField(serializers.FileField):
#    type_name = "FilePathField"
#    widget = forms.TextInput
#
#    def __init__(self, *args, **kwargs):
#        kwargs['required'] = False
#        kwargs['allow_empty_file'] = True
#        super(FilePathField, self).__init__(*args, **kwargs)
#
#    def from_native(self, data):
#        return data


class GrowthSerializer(serializers.ModelSerializer):
    """
    Serializes the growth model.

    """
    growth = serializers.CharField(max_length=50)
    #sample = serializers.CharField(max_length=50)
    #height = FilePathField(max_length=150)
    #amplitude = FilePathField(max_length=150)

    def transform_growth(self, obj, value):
        return value

    def validate_growth(self, attrs, source):
        print(source)
        print(attrs)
        try:
            growth = growths.models.growth.get_growth(attrs[source])
        except Exception as e:
            raise serializers.ValidationError(str(e))

        attrs[source] = growth
        return attrs

    #def transform_sample(self, obj, value):
    #    return value
    #
    #def validate_sample(self, attrs, source):
    #    growth_object = None
    #    if type(attrs['growth']) is not str:
    #        growth_object = attrs['growth']
    #    try:
    #        sample = growths.models.sample.get_sample(attrs[source], growth_object)
    #    except Exception as e:
    #        raise serializers.ValidationError(str(e))
    #
    #    attrs[source] = sample
    #    return attrs

    class Meta:
        model = growth
        fields = ('id', 'growth_number', 'date', 'operator', 'project', 'investigation',
                  'platter', 'reactor', 'run_comments')

class ReadingsSerializer(serializers.ModelSerializer):
    """
    Serializes the readings model.

    """
    growthid = serializers.IntegerField()
    #sample = serializers.CharField(max_length=50)
    #height = FilePathField(max_length=150)
    #amplitude = FilePathField(max_length=150)

    #def transform_growth(self, obj, value):
    #    return value
    #
    #def validate_growth(self, attrs, source):
    #    try:
    #        growth = growths.models.growth.get_growth(attrs[source])
    #    except Exception as e:
    #        raise serializers.ValidationError(str(e))
    #
    #    attrs[source] = growth
    #    return attrs

    #def transform_sample(self, obj, value):
    #    return value
    #
    #def validate_sample(self, attrs, source):
    #    growth_object = None
    #    if type(attrs['growth']) is not str:
    #        growth_object = attrs['growth']
    #    try:
    #        sample = growths.models.sample.get_sample(attrs[source], growth_object)
    #    except Exception as e:
    #        raise serializers.ValidationError(str(e))
    #
    #    attrs[source] = sample
    #    return attrs

    class Meta:
        model = readings
        fields = ('id', 'growth', 'layer', 'layer_desc', 'pyro_out', 'pyro_in', 'tc_in', 'tc_out', 'motor_rpm',
                  'gc_pressure', 'gc_position', 'voltage_in', 'current_in', 'voltage_out', 'current_out',
                  'top_vp_flow', 'hydride_inner', 'hydride_outer', 'alkyl_flow_inner', 'alkyl_push_inner',
                  'alkyl_flow_middle', 'alkyl_push_middle', 'alkyl_flow_outer',  'alkyl_push_outer',
                  'n2_flow', 'h2_flow', 'nh3_flow', 'hydride_pressure', 'tmga1_flow', 'tmga1_pressure',
                  'tmga2_flow', 'tmga2_pressure', 'tega2_flow', 'tega2_pressure', 'tmin1_flow',
                  'tmin1_pressure', 'tmal1_flow', 'tmal1_pressure', 'cp2mg_flow', 'cp2mg_pressure',
                  'cp2mg_dilution', 'silane_flow', 'silane_dilution', 'silane_mix', 'silane_pressure', 'ecp_temp')