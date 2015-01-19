# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from core.models import Substrate, Sample


class SubstrateForm(forms.ModelForm):

    class Meta:
        model = Substrate
        fields = ('comment', 'source', 'serial',)


class SampleForm(forms.ModelForm):

    class Meta:
        model = Sample
        fields = ('substrate','comment',)

    def save(self, commit=True):
        substrate = self.cleaned_data.get('substrate', None)
        comment = self.cleaned_data.get('comment', '')
        instance = Sample.objects.create(substrate, comment)

        if commit:
            instance.save()

        return instance


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
