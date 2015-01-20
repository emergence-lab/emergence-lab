# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import D180Growth, D180Source
from core.forms import ChecklistForm


class WizardBasicInfoForm(forms.ModelForm):

    class Meta:
        model = D180Growth
        fields = ('user', 'investigations', 'platter',)


class WizardGrowthInfoForm(forms.ModelForm):

    class Meta:
        model = D180Growth
        fields = ('has_gan', 'has_aln', 'has_inn', 'has_algan',
                  'has_ingan', 'other_material', 'orientation',
                  'is_template', 'is_buffer', 'has_pulsed',
                  'has_superlattice', 'has_mqw', 'has_graded',
                  'has_u', 'has_n', 'has_p',)
        labels = {
            'has_gan': _('Has GaN'),
            'has_aln': _('Has AlN'),
            'has_inn': _('Has InN'),
            'has_algan': _('Has AlGaN'),
            'has_ingan': _('Has InGaN'),
            'other_material': _('Has other material'),
            'orientation': _('Crystal orientation'),
            'is_template': _('Is the growth a template?'),
            'is_buffer': _('Is the growth a buffer?'),
            'has_pulsed': _('Does the growth include pulsed layer(s)?'),
            'has_superlattice': _('Does the growth include '
                                  'superlattice layers?'),
            'has_mqw': _('Does the growth include multi quantum well layers?'),
            'has_graded': _('Does the growth include graded layer(s)?'),
            'has_n': _('Does the growth include n-doped layer(s)?'),
            'has_u': _('Does the growth include '
                       'unintentionally-doped layer(s)?'),
            'has_p': _('Does the growth include p-doped layer(s)?'),
        }

    def clean(self):
        cleaned_data = super(WizardGrowthInfoForm, self).clean()
        material_fields = ['has_gan', 'has_aln', 'has_algan', 'other_material']
        materials = [field for field in material_fields if cleaned_data[field]]
        if not materials:
            raise forms.ValidationError('At least one material must be specified')

        doping_fields = ['has_n', 'has_p', 'has_u']
        doping = [field for field in doping_fields if cleaned_data[field]]
        if not doping:
            raise forms.ValidationError('At least one doping type must be specified')

        return cleaned_data


class WizardFullForm(forms.ModelForm):

    class Meta:
        model = D180Growth
        fields = ('user', 'investigations', 'platter', 'comment',
                  'has_gan', 'has_aln', 'has_inn', 'has_algan',
                  'has_ingan', 'other_material', 'orientation',
                  'is_template', 'is_buffer', 'has_pulsed',
                  'has_superlattice', 'has_mqw', 'has_graded',
                  'has_n', 'has_p', 'has_u',)

    def clean(self):
        cleaned_data = super(WizardFullForm, self).clean()
        material_fields = ['has_gan', 'has_aln', 'has_algan', 'other_material']
        materials = [field for field in material_fields if cleaned_data[field]]
        if not materials:
            raise forms.ValidationError('At least one material must be specified')

        doping_fields = ['has_n', 'has_p', 'has_u']
        doping = [field for field in doping_fields if cleaned_data[field]]
        if not doping:
            raise forms.ValidationError('At least one doping type must be specified')

        return cleaned_data


class StartGrowthForm(forms.ModelForm):
    class Meta:
        model = D180Growth
        fields = ['user', 'platter']

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
        fields = ('user', 'comment', 'investigations', 'platter',
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


class WizardPrerunChecklistForm(ChecklistForm):
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


class SourcesForm(forms.ModelForm):

    class Meta:
        model = D180Source
        fields = ('cp2mg', 'tmin1', 'tmin2', 'tmga1', 'tmga2', 'tmal1',
                  'tega1', 'nh3', 'sih4',)
        labels = {
            'cp2mg': _('Cp2Mg'),
            'tmin1': _('TMIn #1'),
            'tmin2': _('TMIn #2'),
            'tmga1': _('TMGa #1'),
            'tmga2': _('TMGa #2'),
            'tmal1': _('TMAl #1'),
            'tega1': _('TEGa #1'),
            'nh3': _('NH3'),
            'sih4': _('SiH4'),
        }


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


class CommentsForm(forms.Form):
    comment = forms.CharField(
        label="Run Comments",
        required=False,
        widget=forms.Textarea(attrs={'class': 'hallo'}))
