from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from growth.models import growth, sample

# Create the form class.
# class sample_form(ModelForm):
#     class Meta:
#         model = growth
#         fields = ['substrate_type', 'substrate_serial', 'substrate_orientation', 'substrate_miscut',
#                   'size']
# class growth_form(ModelForm):
#     class Meta:
#         model = sample