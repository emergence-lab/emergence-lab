# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import six

from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import ugettext_lazy as _

from betterforms import multiform

from core.models import Substrate, Sample


class SubstrateForm(forms.ModelForm):
    """
    Form to create a substrate. At least one field must have data to validate.
    """
    comment = forms.CharField(
        label="Substrate Comments",
        required=False,
        widget=forms.Textarea(attrs={'class': 'hallo'}))

    class Meta:
        model = Substrate
        fields = ('comment', 'source', 'serial',)

    def clean(self):
        cleaned_data = super(SubstrateForm, self).clean()
        data = [cleaned_data.get('comment'),
                cleaned_data.get('source'),
                cleaned_data.get('serial')]

        if not any(data):
            raise ValidationError(_('Cannot leave all substrate fields blank.'))


class SampleForm(forms.ModelForm):
    """
    Form to create a new sample using an already existing substrate.
    """
    comment = forms.CharField(
        label="Sample Comments",
        required=False,
        widget=forms.Textarea(attrs={'class': 'hallo'}))

    class Meta:
        model = Sample
        fields = ('comment',)


class SampleMultiForm(multiform.MultiModelForm):
    form_classes = {
        'substrate': SubstrateForm,
        'sample': SampleForm,
    }


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

        # check if existing sample specified
        uuid = cleaned_data.get('sample_uuid')
        if uuid:
            try:
                cleaned_data['sample'] = Sample.objects.get_by_uuid(uuid)
                if uuid[-1].isalpha():  # specified piece
                    if uuid[-1] not in cleaned_data['sample'].pieces:
                        self.add_error('sample_uuid',
                            'Sample {} does not have piece {}'.format(
                                uuid[:-1], uuid[-1]))
                    cleaned_data['piece'] = uuid[-1]
                else:
                    if len(cleaned_data['sample'].pieces) > 1:
                        self.add_error('sample_uuid',
                            'Sample {} is ambiguous, piece '
                            'needs to be specified'.format(uuid))
                cleaned_data['piece'] = uuid[-1] if uuid[-1].isalpha() else 'a'
            except ObjectDoesNotExist:
                self.add_error('sample_uuid',
                               'Sample {} not found'.format(uuid))
                return
        else:
            cleaned_data['sample'] = None
            cleaned_data['piece'] = 'a'

        # cannot create new sample and specify existing sample
        if cleaned_data.get('sample') is not None:
            if any([cleaned_data.get('sample_comment'),
                    cleaned_data.get('substrate_comment'),
                    cleaned_data.get('substrate_source'),
                    cleaned_data.get('substrate_serial')]):
                raise ValidationError('Existing sample cannot be specified in '
                                      'addition to creating a new sample')
        else:
            substrate_data = {
                'comment': cleaned_data.get('substrate_comment'),
                'serial': cleaned_data.get('substrate_serial'),
                'source': cleaned_data.get('substrate_source'),
            }
            substrate_form = SubstrateForm(data=substrate_data)
            if not substrate_form.is_valid():
                for field, error in six.iteritems(substrate_form.errors):
                    if field == '__all__':
                        self.add_error(None, error)
                    else:
                        self.add_error('substrate_{}'.format(field), error)

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
            if not substrate.serial:
                substrate.serial = 'WBG-{}'.format(sample.uuid[1:])
                substrate.save()
            self.instance = sample
        else:
            self.instance = self.cleaned_data['sample']
        return self.instance


SampleFormSet = forms.formsets.formset_factory(
    SampleSelectOrCreateForm, min_num=1, extra=0, validate_min=True)


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
