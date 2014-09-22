from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from growths.models import growth, sample, readings, source
import time
import re
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from core.validators import*

from core.forms import MarkdownField


# Create the form class.
class sample_form(ModelForm):
    parent = forms.CharField(label="Parent Sample (leave empty if there is no parent)", required=False)
    comment = MarkdownField(required=False)

    class Meta:
        model = sample
        fields = ['parent', 'substrate_type', 'substrate_serial', 'substrate_orientation',
                  'substrate_miscut', 'size', 'location', 'comment']

    def clean_parent(self):
        parent_name = self.cleaned_data['parent']

        if parent_name == '':  # no parent specified, on substrate
            return None

        try:
            parent_sample = sample.get_sample(parent_name)
        except Exception as e:
            raise forms.ValidationError(str(e))

        return parent_sample

    def save(self, **kwargs):
        commit = kwargs.pop('commit', True)
        growth_obj = kwargs.pop('growth')
        pocket = kwargs.pop('pocket')

        instance = super(sample_form, self).save(commit=False)
        instance.growth = growth_obj
        instance.pocket = pocket

        if commit:
            instance.save()

        if instance.parent is None:
            instance.parent = instance
        else:
            instance.parent.location = 'Consumed'
            instance.substrate_type = 'growth'
            instance.substrate_serial = instance.parent.substrate_serial
            instance.substrate_orientation = instance.parent.substrate_orientation
            instance.substrate_miscut = instance.parent.substrate_miscut
            instance.size = instance.parent.size

        if commit:
            instance.save()
            if instance.parent != instance:
                instance.parent.save()
        return instance


class growth_form(ModelForm):
    class Meta:
        model = growth
        fields = ['growth_number', 'date', 'operator', 'project', 'investigation',
                  'platter', 'reactor', 'run_comments', 'has_gan', 'has_aln', 'has_inn',
                  'has_algan', 'has_ingan', 'has_alingan', 'other_material', 'orientation',
                  'is_template', 'is_buffer', 'has_superlattice', 'has_mqw', 'has_graded',
                  'has_n', 'has_p', 'has_u']


class GrowthUpdateForm(ModelForm):
    run_comments = MarkdownField()

    class Meta:
        model = growth
        fields = ('run_comments', 'has_gan', 'has_algan', 'has_aln',
                  'other_material', 'is_template', 'is_buffer', 'has_n',
                  'has_p', 'has_u',)


class p_form(forms.Form):
    add_sample = forms.BooleanField(required=False)


class start_growth_form(ModelForm):
    class Meta:
        model = growth
        fields = ['growth_number', 'date', 'operator', 'project', 'investigation',
                  'platter', 'reactor']

    def clean_growth_number(self):
        growth_number = self.cleaned_data['growth_number']
        m = re.match('^([gt][1-9][0-9]{3,})$', growth_number)
        if not m:
            raise forms.ValidationError('Growth {0} improperly formatted. Did you accidently include the growth tag?'.format(growth_number))

        return growth_number


    def save(self, *args, **kwargs):
        commit = kwargs.pop('commit', True)
        comments = kwargs.pop('runcomments')
        instance = super(start_growth_form, self).save(*args, commit=False, **kwargs)
        if commit:
            instance.save()
        instance.run_comments = comments
        instance.save()
        return instance


class prerun_growth_form(ModelForm):
    class Meta:
        model = growth
        exclude = ['growth_number', 'date', 'operator', 'run_comments',
                   'has_inn', 'has_ingan', 'has_alingan']

    def clean(self):
        cleaned_data = super(prerun_growth_form, self).clean()
        material_fields = ['has_gan', 'has_aln', 'has_algan', 'other_material']
        materials = [field for field in material_fields if cleaned_data[field]]
        if not materials:
            raise ValidationError('At least one material must be specified')

        doping_fields = ['has_n', 'has_p', 'has_u']
        doping = [field for field in doping_fields if cleaned_data[field]]
        if not doping:
            raise ValidationError('At least one doping type must be specified')

        return cleaned_data


class prerun_checklist_form(forms.Form):
    field_1 = forms.BooleanField(required=True, label="Is Run Ready? Comments Updated?")
    field_2 = forms.BooleanField(required=True, label="Engage Load Lock Routine?")
    field_3 = forms.BooleanField(required=True, label="Load the wafers (Note Substrate number / Run number / Single side / Double side in space provided below)?")
    field_4 = forms.BooleanField(required=True, label="Close LL?")
    field_5 = forms.BooleanField(required=True, label="Check from recipe the required Alkyl Sources and make sure they are open?")
    field_6 = forms.BooleanField(required=True, label="Check from recipe the required Hydrides(including Silane) and make sure they are open?")
    field_7 = forms.BooleanField(required=True, label="Check and note LL Pressure (must be < 1E-5)?")
    field_8 = forms.BooleanField(required=True, label="Engage Gate Valve Routing? Open Front VP and Shutter?")
    field_9 = forms.BooleanField(required=True, label="Transfer wafer carrier to the reactor?")
    field_10 = forms.BooleanField(required=True, label="Check for Rotation?")
    field_11 = forms.BooleanField(required=True, label="Close Gate Valve, Front VP and Shutter?")
    field_12 = forms.BooleanField(required=True, label="System IDLE? Correct Recipe Loaded? Power Supply On? Motor on Auto? GC Pressure Remote?")
    field_13 = forms.BooleanField(required=True, label="Start the Run?")
    field_14 = forms.BooleanField(required=True, label="Start the Epimetric?")


class prerun_sources_form(ModelForm):
    class Meta:
        model = source


class postrun_checklist_form(forms.Form):
    field_1 = forms.BooleanField(required=True, label="Wait for system to IDLE?")
    field_2 = forms.BooleanField(required=True, label="Save Epimetric data?")
    field_3 = forms.BooleanField(required=True, label="Turn off motor")
    field_4 = forms.BooleanField(required=True, label="Engage Gate Valve Routine? Open Front VP and Shutter?")
    field_5 = forms.BooleanField(required=True, label="Transfer Wafer carrier from the Reactor to LL?")
    field_6 = forms.BooleanField(required=True, label="Close Gate Valve?")
    field_7 = forms.BooleanField(required=True, label="Check and note LL Pressure(must be < 1E-5)?")
    field_8 = forms.BooleanField(required=True, label="Engage LL Routine?")
    field_9 = forms.BooleanField(required=True, label="Unload the wafers and updated comments and observations in the space provided below? Close LL?")
    field_10 = forms.BooleanField(required=True, label="Close Bubblers if done using them?")


class split_form(ModelForm):
    pieces = forms.IntegerField(label="Number of pieces", validators=[validate_not_zero])
    parent = forms.CharField(label="Sample to split")

    class Meta:
        model = sample
        fields = ['parent', 'pieces']

    def clean_parent(self):
        try:
            obj = sample.get_sample(self.cleaned_data['parent'])
            return obj
        except Exception as e:
            raise forms.ValidationError(str(e))


class readings_form(ModelForm):
    class Meta:
        model = readings
        exclude = ['growth']


class comments_form(forms.Form):
    comment_field = MarkdownField(label="Run Comments", required=False)
