# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from core.forms import ChecklistForm
from core.models import Process
from d180.models import D180Readings, D180Source, D180GrowthInfo, Platter


class WizardBasicProcessForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(WizardBasicProcessForm, self).__init__(*args, **kwargs)
        self.fields['milestones'] = forms.MultipleChoiceField(required=False, choices=[
            ('{} - {}'.format(i.project.name, i.name), [(m.id, m.name) for m in i.milestones.all()])
            for i in user.get_investigations('member') if i.milestones.exists()
        ])
        self.fields['investigations'] = forms.MultipleChoiceField(required=False, choices=[
            (p.name, [(i.id, i.name) for i in p.investigations.all()])
            for p in user.get_projects('member') if p.investigations.exists()
        ])

    class Meta:
        model = Process
        fields = ('user', 'type', 'legacy_identifier', 'investigations', 'milestones')
        widgets = {
            'type': forms.HiddenInput(),
        }


class WizardGrowthInfoForm(forms.ModelForm):

    platter = forms.ModelChoiceField(required=True,
                                     queryset=Platter.active_objects.all())

    class Meta:
        model = D180GrowthInfo
        fields = ('platter',
                  'has_gan', 'has_aln', 'has_inn', 'has_algan',
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

        doping_fields = ['has_n', 'has_p', 'has_u']
        doping = [field for field in doping_fields if cleaned_data[field]]

        # collect validation errors
        errors = []
        if not materials:
            errors.append(forms.ValidationError(_('At least one material must be specified'),
                                                code='material'))
        if not doping:
            errors.append(forms.ValidationError(_('At least one doping type must be specified'),
                                                code='doping'))
        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data


class WizardFullProcessForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WizardFullProcessForm, self).__init__(*args, **kwargs)
        self.fields['milestones'].required = False

    class Meta:
        model = Process
        fields = ('user', 'investigations', 'title', 'comment',
                  'legacy_identifier', 'type', 'milestones', )


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
        'Set up k-space settings and start run',
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


class D180ReadingsForm(forms.ModelForm):

    class Meta:
        model = D180Readings
        fields = ('layer', 'description',
                  'pyro_out', 'pyro_in', 'ecp_temp', 'tc_out', 'tc_in',
                  'motor_rpm', 'gc_pressure', 'gc_position', 'voltage_in',
                  'voltage_out', 'current_in', 'current_out', 'top_vp_flow',
                  'hydride_inner', 'hydride_outer', 'alkyl_flow_inner',
                  'alkyl_push_inner', 'alkyl_flow_middle', 'alkyl_push_middle',
                  'alkyl_flow_outer', 'alkyl_push_outer', 'n2_flow', 'h2_flow',
                  'nh3_flow', 'hydride_pressure', 'tmga1_flow',
                  'tmga1_pressure', 'tmga2_flow', 'tmga2_pressure',
                  'tega2_flow', 'tega2_pressure', 'tmin1_flow',
                  'tmin1_pressure', 'tmal1_flow', 'tmal1_pressure',
                  'cp2mg_flow', 'cp2mg_pressure', 'cp2mg_dilution',
                  'silane_flow', 'silane_dilution', 'silane_mix',
                  'silane_pressure',)
        labels = {
            'layer': _('Layer number'),
            'description': _('Layer description'),
            'pyro_out': _('Outer pyro [°C]'),
            'pyro_in': _('Inner pyro [°C]'),
            'ecp_temp': _('ECP temperature [°C]'),
            'tc_out': _('Outer thermocouple temperature [°C]'),
            'tc_in': _('Inner thermocouple temperature [°C]'),
            'motor_rpm': _('Motor speed [RPM]'),
            'gc_pressure': _('Growth chamber pressure [torr]'),
            'gc_position': _('Throttle valve position [%]'),
            'voltage_in': _('Inner filament voltage [V]'),
            'voltage_out': _('Outer filament voltage [V]'),
            'current_in': _('Inner filament current [A]'),
            'current_out': _('Outer filament current [A]'),
            'top_vp_flow': _('Top viewport flow [sccm]'),
            'hydride_inner': _('Inner hydride flow [sccm]'),
            'hydride_outer': _('Outer hydride flow [sccm]'),
            'alkyl_flow_inner': _('Inner alkyl flow [sccm]'),
            'alkyl_push_inner': _('Inner alkyl push [sccm]'),
            'alkyl_flow_middle': _('Middle alkyl flow [sccm]'),
            'alkyl_push_middle': _('Middle alkyl push [sccm]'),
            'alkyl_flow_outer': _('Outer alkyl flow [sccm]'),
            'alkyl_push_outer': _('Outer alkyl push [sccm]'),
            'n2_flow': _('N2 flow [sccm]'),
            'h2_flow': _('H2 flow [sccm]'),
            'nh3_flow': _('NH3 flow [sccm]'),
            'hydride_pressure': _('Hydride pressure [torr]'),
            'tmga1_flow': _('TMGa #1 flow [sccm]'),
            'tmga1_pressure': _('TMGa #1 pressure [torr]'),
            'tmga2_flow': _('TMGa #2 flow [sccm]'),
            'tmga2_pressure': _('TMGa #2 pressure [torr]'),
            'tega2_flow': _('TEGa #1 flow [sccm]'),
            'tega2_pressure': _('TEGa #1 pressure [torr]'),
            'tmin1_flow': _('TMIn #1 flow [sccm]'),
            'tmin1_pressure': _('TMIn #1 pressure [torr]'),
            'tmal1_flow': _('TMAl #1 flow [sccm]'),
            'tmal1_pressure': _('TMAl #1 pressure [torr]'),
            'cp2mg_flow': _('Cp2Mg flow [sccm]'),
            'cp2mg_pressure': _('Cp2Mg pressure [torr]'),
            'cp2mg_dilution': _('Cp2Mg dilution [sccm]'),
            'silane_flow': _('Silane flow [sccm]'),
            'silane_dilution': _('Silane dilution [sccm]'),
            'silane_mix': _('Silane mix [sccm]'),
            'silane_pressure': _('Silane pressure [torr]'),
        }

    def save(self, process, commit=True):
        self.instance = super(D180ReadingsForm, self).save(commit=False)
        self.instance.process = process
        if commit:
            self.instance.save()

        return self.instance


D180ReadingsFormSet = forms.models.modelformset_factory(D180Readings,
                                                        D180ReadingsForm)


class WizardPostrunChecklistForm(ChecklistForm):
    checklist_fields = [
        'Wait for system to IDLE',
        'Stop k-space collection',
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
    title = forms.CharField(label='Short Run Description', required=True)
    comment = forms.CharField(
        label="Additional Run Comments",
        required=False,
        widget=forms.Textarea(attrs={'class': 'hallo'}))


class ReservationCloseForm(forms.Form):
    hold_open = forms.BooleanField(
        required=False,
        label=_('Hold the reservation'))
