import re

from django import forms
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import afm
from growths.models import growth, sample
import growths.models


class afm_form(forms.ModelForm):
    """
    Form for afm creation.
    """
    growth = forms.CharField()
    sample = forms.CharField()

    def clean_growth(self):
        """
        Validate growth number from user input and put a growth object in the form data.
        """
        growth_number = self.cleaned_data['growth']

        m = re.match('[gt][1-9][0-9]{3,}', growth_number)
        if not m:
            raise forms.ValidationError('Growth {0} improperly formatted'.format(growth_number))

        try:
            self.cleaned_data['growth'] = growth.objects.get(growth_number=growth_number)
        except MultipleObjectsReturned as e:
            raise forms.ValidationError('Growth {0} ambiguous'.format(growth_number))
        except ObjectDoesNotExist as e:
            raise forms.ValidationError('Growth {0} does not exist'.format(growth_number))

        return self.cleaned_data['growth']

    def clean_sample(self):
        """
        Validate sample number from user input and put a sample object in the form data.
        """

        sample_name = self.cleaned_data['sample']

        # extract information from sample name
        m = re.match('([gt][1-9][0-9]{3,})(?:\_([1-6])([a-z]*))?', sample_name)
        if not m:
            raise forms.ValidationError('Sample {0} improperly formatted'.format(sample_name))

        # check if growth number and sample growth number match
        if 'growth' not in self.cleaned_data or m.group(1) != self.cleaned_data['growth'].growth_number:
            raise forms.ValidationError('Sample {0} does not match the growth'.format(sample_name))
        kwargs = {'growth': self.cleaned_data['growth']}

        # check if pocket or piece are specified
        if m.group(2):
            kwargs['pocket'] = int(m.group(2))
        if m.group(3):
            kwargs['piece'] = m.group(3)
        print(kwargs)

        try:
            self.cleaned_data['sample'] = sample.objects.get(**kwargs)
        except MultipleObjectsReturned as e:
            raise forms.ValidationError('Sample {0} ambiguous, specify the pocket or piece'.format(sample_name))
        except ObjectDoesNotExist as e:
            raise forms.ValidationError('Sample {0} does not exist'.format(sample_name))

        return self.cleaned_data['sample']

    class Meta:
        model = afm
        fields = ['growth', 'sample', 'scan_number', 'rms', 'zrange',
                  'location', 'size', 'filename', 'amplitude_filename', ]
