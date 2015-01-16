# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import D180Growth, D180Source
from core.forms import ChecklistForm


class GrowthForm(forms.ModelForm):

    class Meta:
        model = D180Growth
        fields = ('uuid', 'created', 'modified', 'user',
                  'investigations', 'platter', 'comment',
                  'has_gan', 'has_aln', 'has_inn', 'has_algan',
                  'has_ingan', 'other_material', 'orientation',
                  'is_template', 'is_buffer', 'has_pulsed',
                  'has_superlattice', 'has_mqw', 'has_graded',
                  'has_n', 'has_p', 'has_u',)


class AddSampleForm(forms.Form):
    add_sample = forms.BooleanField(required=False)


class StartGrowthForm(forms.ModelForm):
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


class PrerunGrowthForm(forms.ModelForm):

    class Meta:
        model = D180Growth
        fields = ('uuid', 'user', 'comment', 'investigations', 'platter',
                  'has_gan', 'has_aln', 'has_inn', 'has_algan', 'has_ingan',
                  'other_material', 'orientation',
                  'is_template', 'is_buffer', 'has_pulsed', 'has_superlattice',
                  'has_mqw', 'has_graded', 'has_n', 'has_u', 'has_p',)

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


class PrerunSourcesForm(forms.ModelForm):

    class Meta:
        model = D180Source
        fields = ('cp2mg', 'tmin1', 'tmin2', 'tmga1', 'tmga2', 'tmal1',
                  'tega1', 'nh3', 'sih4',)


class PostrunChecklistForm(forms.ChecklistForm):
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


class CommentsForm(forms.Form):
    comment_field = forms.CharField(widget=CKEditorWidget(), label="Run Comments", required=False)
