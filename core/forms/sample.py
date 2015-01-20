# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from core.models import Substrate, Sample


class SubstrateForm(forms.ModelForm):

    class Meta:
        model = Substrate
        fields = ('comment', 'source', 'serial',)


class SampleForm(forms.ModelForm):

    class Meta:
        model = Sample
        fields = ('substrate', 'comment',)

    def save(self, commit=True):
        substrate = self.cleaned_data.get('substrate', None)
        comment = self.cleaned_data.get('comment', '')
        instance = Sample.objects.create(substrate, comment)

        if commit:
            instance.save()

        return instance


class SampleSelectOrCreateForm(forms.Form):
    # use existing sample
    sample_uuid = forms.CharField(required=False)

    # create new sample
    sample_comment = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'class': 'hallo'}))
    substrate_comment = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'class': 'hallo'}))
    substrate_source = forms.CharField(required=False)
    substrate_serial = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(SampleSelectOrCreateForm, self).clean()
        uuid = cleaned_data['sample_uuid']

        if uuid:
            try:
                sample = Sample.objects.get_by_uuid(uuid)
                cleaned_data['sample'] = sample
                self.instance = sample
            except ObjectDoesNotExist:
                raise ValidationError('Sample {} not found'.format(uuid))
        else:
            cleaned_data['sample'] = None

        return cleaned_data

    def save(self, commit=True):
        if self.cleaned_data['sample'] is None:
            substrate_kwargs = {
                'comment': self.cleaned_data['substrate_comment'],
                'serial': self.cleaned_data['substrate_serial'],
                'source': self.cleaned_data['substrate_source'],
            }
            substrate = Substrate.objects.create(**substrate_kwargs)
            comment = self.cleaned_data['sample_comment']
            sample = Sample.objects.create(substrate=substrate, comment=comment)
            self.instance = sample
        return self.instance


SampleFormSet = forms.formsets.formset_factory(SampleSelectOrCreateForm)


class SplitSampleForm(forms.ModelForm):
    pieces = forms.IntegerField(label="Number of pieces")
    sample = forms.CharField(label="Sample to split")

    class Meta:
        model = Sample
        fields = ('sample', 'pieces',)

    def clean_pieces(self):
        if self.cleaned_data['pieces'] <= 1:
            raise forms.ValidationError('Number of pieces must be greater than 1')
        return self.cleaned_data['pieces']

    def clean_sample(self):
        try:
            obj = Sample.objects.get_by_uuid(self.cleaned_data['sample'])
            return obj
        except Exception as e:
            raise forms.ValidationError(str(e))


class SampleSizeForm(forms.Form):
    SIZE_CHOICES = [
        ('whole', 'Whole'),
        ('half', 'Half'),
        ('quarter', 'Quarter'),
        ('square_cm', 'Square cm'),
        ('other', 'Other'),
    ]

    def __init__(self, *args, **kwargs):
        samples = kwargs.pop('samples', [])
        super(SampleSizeForm, self).__init__(*args, **kwargs)

        for i, sample in enumerate(samples):
            self.fields['{}'.format(sample)] = forms.ChoiceField(choices=self.SIZE_CHOICES)
