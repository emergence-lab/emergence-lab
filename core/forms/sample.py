# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from betterforms import multiform
from crispy_forms import helper, layout, bootstrap

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
    existing_or_new = forms.ChoiceField(
        required=True,
        label=_('Sample Type'),
        choices=[
            ('existing-sample', 'Use Existing Sample'),
            ('new-sample', 'Create New Sample')],
        widget=forms.RadioSelect())

    # use existing sample
    sample_uuid = forms.CharField(
        required=False,
        label=_('Sample UUID'))

    # create new sample
    sample_comment = forms.CharField(
        required=False,
        label=_('Sample Comment'),
        widget=forms.Textarea(attrs={'class': 'hallo'}))
    substrate_comment = forms.CharField(
        required=False,
        label=_('Substrate Comment'),
        widget=forms.Textarea(attrs={'class': 'hallo'}))
    substrate_source = forms.CharField(
        required=False,
        label=_('Substrate Source or Vendor'))
    substrate_serial = forms.CharField(
        required=False,
        label=_('Substrate Serial Number'))

    def __init__(self, *args, **kwargs):
        super(SampleSelectOrCreateForm, self).__init__(*args, **kwargs)
        prefix = kwargs.get('prefix', '')
        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = layout.Layout(
            bootstrap.InlineRadios('existing_or_new'),
            layout.Div(
                layout.Field('sample_uuid'),
                id='new-sample_{}'.format(prefix)
            ),
            layout.Div(
                layout.Field('sample_comment', css_class='hallo'),
                layout.Field('substrate_comment', css_class='hallo'),
                layout.Field('substrate_source'),
                layout.Field('substrate_serial'),
                id='existing-sample_{}'.format(prefix)
            ),
        )

    def clean(self):
        cleaned_data = super(SampleSelectOrCreateForm, self).clean()
        existing_or_new = cleaned_data.get('existing_or_new')
        if not existing_or_new:
            raise ValidationError({'existing_or_new', 'This field is required.'})

        # Use existing sample
        if existing_or_new == 'existing-sample':
            try:
                uuid = cleaned_data.get('sample_uuid')
                if not uuid:
                    self.add_error(
                        'sample_uuid',
                        'This field is required when existing sample is selected')
                pk, piece = Sample.strip_uuid(uuid)
                sample = Sample.objects.get_by_uuid(uuid)
                if piece is None:  # piece not specified
                    piece = 'a'
                    if sample.pieces.count() > 1:
                        self.add_error('sample_uuid',
                            'Sample {} is ambiguous, '
                            'piece needs to be specified'.format(sample.uuid))
                elif piece not in sample.pieces:  # piece specified, doesn't exist
                    self.add_error(
                        'sample_uuid',
                        'Sample {} does not have a piece {}'.format(sample.uuid,
                                                                    piece))
                cleaned_data['sample'] = sample
                cleaned_data['piece'] = piece
            except Sample.DoesNotExist:
                self.add_error('sample_uuid', 'Sample {} not found'.format(uuid))
                cleaned_data['sample'] = None
                cleaned_data['piece'] = 'a'

        # Create new sample
        elif existing_or_new == 'new-sample':
            cleaned_data['sample'] = None
            cleaned_data['piece'] = 'a'
            substrate_data = {
                'comment': cleaned_data.get('substrate_comment'),
                'serial': cleaned_data.get('substrate_serial'),
                'source': cleaned_data.get('substrate_source'),
            }
            substrate_form = SubstrateForm(data=substrate_data)
            if not substrate_form.is_valid():
                for field, error in substrate_form.errors.items():
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
