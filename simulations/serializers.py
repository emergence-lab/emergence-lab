from django import forms
from rest_framework import serializers

from .models import Simulation


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


class SimSerializer(serializers.ModelSerializer):
    """
    Serializes the Sim model.

    """
    #growth = serializers.CharField(max_length=50)
    #sample = serializers.CharField(max_length=50)
    #height = FilePathField(max_length=150)
    #amplitude = FilePathField(max_length=150)
    #
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
    #
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
        model = Simulation
        fields = ('id', 'user', 'request_date', 'start_date', 'finish_date',
                  'priority', 'execution_node')
