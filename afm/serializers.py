from django import forms
from rest_framework import serializers

from .models import afm
import growths.models

class FilePathField(serializers.FileField):
    type_name = "FilePathField"
    widget = forms.TextInput

    def from_native(self, data):
        return data

class AFMSerializer(serializers.ModelSerializer):
    """
    Serializes the afm model.

    """
    growth = serializers.CharField(max_length=50)
    sample = serializers.CharField(max_length=50)
    height = FilePathField(max_length=150, required=False, allow_empty_file=True)

    def transform_growth(self, obj, value):
        return value

    def validate_growth(self, attrs, source):
        try:
            growth = growths.models.growth.get_growth(attrs[source])
        except Exception as e:
            raise serializers.ValidationError(str(e))

        attrs[source] = growth
        return attrs

    def transform_sample(self, obj, value):
        return value

    def validate_sample(self, attrs, source):
        growth_object = None
        if type(attrs['growth']) is not str:
            growth_object = attrs['growth']
        try:
            sample = growths.models.sample.get_sample(attrs[source], growth_object)
        except Exception as e:
            raise serializers.ValidationError(str(e))

        attrs[source] = sample
        return attrs

    # def transform_height(self, obj, value):
    #     return 'testing'

    def validate_height(self, attrs, source):
        print(attrs)
        # raise serializers.ValidationError('forced image')
        return attrs

    class Meta:
        model = afm
        fields = ('id', 'growth', 'sample', 'scan_number', 'rms', 'zrange',
                  'location', 'size', 'height')
