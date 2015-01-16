# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import DGrowth, Readings, Source
from core.forms import ChecklistForm
from core.models import ProcessNode


# Create the form class.
class SampleForm(forms.ModelForm):
    parent = forms.CharField(label="Parent Sample (leave empty if there is no parent)", required=False)

    class Meta:
        model = SampleNode
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


class GrowthForm(ModelForm):
    class Meta:
        model = Growth
        fields = ['uid', 'user', 'comment', 'investigations', 'platter',
                  'has_gan', 'has_aln', 'has_inn', 'has_algan', 'has_ingan',
                  'other_material', 'orientation',
                  'is_template', 'is_buffer', 'has_pulsed', 'has_superlattice',
                  'has_mqw', 'has_graded', 'has_n', 'has_u', 'has_p',]


class p_form(forms.Form):
    add_sample = forms.BooleanField(required=False)



class StartGrowthForm(ModelForm):
    class Meta:
        model = D180Growth
        fields = ['uuid', 'user', 'platter']

    def save(self, *args, **kwargs):
        commit = kwargs.pop('commit', True)
        comments = kwargs.pop('comments')
        instance = super(StartGrowthForm, self).save(*args, commit=False, **kwargs)
        instance.comments = comments
        if commit:
            instance.save()
        return instance


class PrerunGrowthForm(ModelForm):
    class Meta:
        model = D180Growth
        fields = ['uuid', 'user', 'comment', 'investigations', 'platter',
                  'has_gan', 'has_aln', 'has_inn', 'has_algan', 'has_ingan',
                  'other_material', 'orientation',
                  'is_template', 'is_buffer', 'has_pulsed', 'has_superlattice',
                  'has_mqw', 'has_graded', 'has_n', 'has_u', 'has_p',]

    def clean(self):
        cleaned_data = super(PrerunGrowthForm, self).clean()
        material_fields = ['has_gan', 'has_aln', 'has_algan', 'other_material']
        materials = [field for field in material_fields if cleaned_data[field]]
        if not materials:
            raise forms.ValidationError('At least one material must be specified')

        doping_fields = ['has_n', 'has_p', 'has_u']
        doping = [field for field in doping_fields if cleaned_data[field]]
        if not doping:
            raise forms.ValidationError('At least one doping type must be specified')

        return cleaned_data


class PrerunChecklistForm(ChecklistForm):
    checklist_fields = [
        'Verify the correct recipe is loaded and comments are updated',
        'Engage load lock routine',
        'Load the wafers',
        'Close load lock',
        'Check required Alkyl Sources (including Cp2Mg) and make sure they are open',
        'Check required Hydrides (including Silane) and make sure they are working',
        'Check load lock pressure (must be < 1E-5)?',
        'Engage gate valve routine, open front viewport and shutter',
        'Transfer platter from load lock to reactor',
        'Check for platter rotation',
        'Close gate valve, front viewport and shutter',
        'Turn on power supplies, set the motor to Auto, and pressure control to Remote',
        'Verify the system is in IDLE',
        'Start the Run and k-space',
    ]


class PrerunSourcesForm(ModelForm):
    class Meta:
        model = D180Source
        fields = ('cp2mg', 'tmin1', 'tmin2', 'tmga1', 'tmga2', 'tmal1',
                  'tega1', 'nh3', 'sih4',)


class PostrunChecklistForm(ChecklistForm):
    checklist_fields = [
        'Wait for system to IDLE',
        'Stop k-space collection'
        'Turn off motor',
        'Engage gate valve routine, open front viewport and shutter',
        'Transfer platter from reactor to load lock',
        'Close gate valve',
        'Check load lock pressure (must be < 1E-5)?',
        'Engage load lock routine',
        'Unload the wafers, update comments and close the load lock',
        'Close Bubblers if done using them',
    ]


class split_form(ModelForm):
    pieces = forms.IntegerField(label="Number of pieces")
    parent = forms.CharField(label="Sample to split")

    class Meta:
        model = sample
        fields = ['parent', 'pieces']

    def clean_pieces(self):
        if self.cleaned_data['pieces'] <= 1:
            raise forms.ValidationError('Number of pieces must be greater than 1')
        return self.cleaned_data['pieces']

    def clean_parent(self):
        try:
            obj = sample.get_sample(self.cleaned_data['parent'])
            return obj
        except Exception as e:
            raise forms.ValidationError(str(e))


class SampleSizeForm(forms.Form):

    def __init__(self, *args, **kwargs):
        samples = kwargs.pop('samples', [])
        super(SampleSizeForm, self).__init__(*args, **kwargs)

        for i, sample_name in enumerate(samples):
            self.fields['{0}'.format(sample_name)] = forms.ChoiceField(choices=sample.SIZE_CHOICES)


class readings_form(ModelForm):
    class Meta:
        model = readings
        exclude = ['growth']


class comments_form(forms.Form):
    comment_field = forms.CharField(widget=CKEditorWidget(), label="Run Comments", required=False)
