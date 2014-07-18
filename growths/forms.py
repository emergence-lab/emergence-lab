from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from growths.models import growth, sample
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
                  'substrate_miscut', 'size']

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
        instance = super(sample_form, self).save(*args, commit = False, **kwargs)
        growthid.date = time.strftime("%Y-%m-%d")
        instance.growth = growthid
        instance.pocket = pocketnum
        if commit:
            print ("saving")
            instance.save()
        if instance.parent == None:
            print ("setting parent to self")
            instance.parent = instance
        instance.substrate_serial = instance.parent.substrate_serial
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
    add_sample = forms.BooleanField()


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

