from django import forms
from django.core.exceptions import ValidationError

from core.models import growth

class afm_search_form(forms.Form):
    growth_number = forms.CharField()
    operator = forms.CharField()
    project = forms.CharField()

    class Meta:
        model = growth
