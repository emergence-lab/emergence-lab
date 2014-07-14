from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from growths.models import growth, sample
import time

# Create the form class.
class sample_form(ModelForm):
    class Meta:
        model = sample
        fields = ['substrate_type', 'substrate_serial', 'substrate_orientation',
                  'substrate_miscut', 'size']
    def save(self, *args, **kwargs):
        print("right here")
        commit = kwargs.pop('commit', True)
        growthid = kwargs.pop('growthid')
        instance = super(sample_form, self).save(*args, commit = False, **kwargs)
        growthid.date = time.strftime("%Y-%m-%d")
        instance.growth = growthid
        print (growthid)
        if commit:
            instance.save()
        return instance

class growth_form(ModelForm):
    class Meta:
        model = growth
        fields = ['growth_number', 'date', 'operator', 'project', 'investigation',
                  'platter', 'reactor', 'run_comments', 'has_gan', 'has_aln', 'has_inn',
                  'has_algan', 'has_ingan', 'has_alingan', 'other_material', 'orientation',
                  'is_template', 'is_buffer', 'has_superlattice', 'has_mqw', 'has_graded',
                  'has_n', 'has_p', 'has_u']
