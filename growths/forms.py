from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from growths.models import growth, sample, readings, source
import time
import re
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from core.validators import*


# Create the form class.
class sample_form(ModelForm):
    parent = forms.CharField(label="Parent Sample (leave empty if there is no parent)", required=False)

    class Meta:
        model = sample
        fields = ['parent', 'substrate_type', 'substrate_serial', 'substrate_orientation',
                  'substrate_miscut', 'size', 'location']

    def clean_parent(self):
        print ("clean sample method running")
        parent_name = self.cleaned_data['parent']
        # check to see if empty (this means that parent is itself). Set a temporary parent value

        if parent_name == '':
            print('setting parent to None')
            return None

            # return self.cleaned_data['parent']

        # extract information from parent name
        m = re.match('([gt][1-9][0-9]{3,})(?:\_([1-6])([a-z]*))?', parent_name)
        if not m:
            raise forms.ValidationError('Sample {0} improperly formatted'.format(parent_name))
        try:
            growth_object = growth.objects.get(growth_number=m.group(1))
        except MultipleObjectsReturned as e:
            raise forms.ValidationError('Possible repeat entry in database (Major Problem! This should never happen. At all.)')
        except ObjectDoesNotExist as e:
            raise forms.ValidationError('Growth {0} does not exist'.format(m.group(1)))
        kwargs = {'growth': growth_object}
        # check if pocket or piece are specified
        if m.group(2):
            kwargs['pocket'] = int(m.group(2))
        if m.group(3):
            kwargs['piece'] = m.group(3)

        try:
            self.cleaned_data['parent'] = sample.objects.get(**kwargs)
        except MultipleObjectsReturned as e:
            raise forms.ValidationError('Sample {0} ambiguous, specify the pocket or piece'.format(parent_name))
        except ObjectDoesNotExist as e:
            raise forms.ValidationError('Sample {0} does not exist'.format(parent_name))

        return self.cleaned_data['parent']

    def save(self, *args, **kwargs):
        print("save method running")
        commit = kwargs.pop('commit', True)
        growthid = kwargs.pop('growthid')
        pocketnum = kwargs.pop('pocketnum')
        instance = super(sample_form, self).save(*args, commit=False, **kwargs)
        growthid.date = time.strftime("%Y-%m-%d")
        instance.growth = growthid
        instance.pocket = pocketnum
        if commit:
            print ("saving")
            instance.save()
        if instance.parent is None:
            print ("setting parent to self")
            instance.parent = instance
        instance.substrate_serial = instance.parent.substrate_serial
        allsamples = sample.objects.filter(substrate_serial=instance.substrate_serial)
        dictionarylist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                          'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        numberofsamples = len(allsamples)
        if numberofsamples > 1:
            instance.piece = dictionarylist[numberofsamples]
        instance.save
        return instance


class growth_form(ModelForm):
    class Meta:
        model = growth
        fields = ['growth_number', 'date', 'operator', 'project', 'investigation',
                  'platter', 'reactor', 'run_comments', 'has_gan', 'has_aln', 'has_inn',
                  'has_algan', 'has_ingan', 'has_alingan', 'other_material', 'orientation',
                  'is_template', 'is_buffer', 'has_superlattice', 'has_mqw', 'has_graded',
                  'has_n', 'has_p', 'has_u']


class p_form(forms.Form):
    add_sample = forms.BooleanField(required=False)


class start_growth_form(ModelForm):
    class Meta:
        model = growth
        fields = ['growth_number', 'date', 'operator', 'project', 'investigation',
                  'platter', 'reactor']


class prerun_growth_form(ModelForm):
    class Meta:
        model = growth
        exclude = ['growth_number', 'date', 'operator']


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
    field_3 = forms.BooleanField(required=True, label="Engage Gate Valve Routine? Open Front VP and Shutter?")
    field_4 = forms.BooleanField(required=True, label="Transfer Wafer carrier from the Reactor to LL?")
    field_5 = forms.BooleanField(required=True, label="Close Gate Valve?")
    field_6 = forms.BooleanField(required=True, label="Check and note LL Pressure(must be < 1E-5)?")
    field_7 = forms.BooleanField(required=True, label="Engage LL Routine?")
    field_8 = forms.BooleanField(required=True, label="Unload the wafers and updated comments and observations in the space provided below? Close LL?")
    field_9 = forms.BooleanField(required=True, label="Close Bubblers if done using them?")


class split_form(ModelForm):
    pieces = forms.IntegerField(label="Number of pieces", validators=[validate_not_zero])
    parent = forms.CharField(label="Sample to split")

    class Meta:
        model = sample
        fields = ['parent', 'pieces']

    def clean_parent(self):
        print ("clean sample method running")
        parent_name = self.cleaned_data['parent']
        # extract information from sample name
        m = re.match('([gt][1-9][0-9]{3,})(?:\_([1-6])([a-z]*))?', parent_name)
        if not m:
            raise forms.ValidationError('Sample {0} improperly formatted'.format(parent_name))
        try:
            growth_object = growth.objects.get(growth_number=m.group(1))
        except MultipleObjectsReturned as e:
            raise forms.ValidationError('Possible repeat entry in database (Major Problem! This should never happen. At all.)')
        except ObjectDoesNotExist as e:
            raise forms.ValidationError('Growth {0} does not exist'.format(m.group(1)))
        kwargs = {'growth': growth_object}
        # check if pocket or piece are specified
        if m.group(2):
            kwargs['pocket'] = int(m.group(2))
        if m.group(3):
            kwargs['piece'] = m.group(3)

        try:
            self.cleaned_data['parent'] = sample.objects.get(**kwargs)
        except MultipleObjectsReturned as e:
            raise forms.ValidationError('Sample {0} ambiguous, specify the pocket or piece'.format(parent_name))
        except ObjectDoesNotExist as e:
            raise forms.ValidationError('Sample {0} does not exist'.format(parent_name))

        return self.cleaned_data['parent']

class readings_form(ModelForm):
    class Meta:
        model = readings
        exclude = ['growth']
