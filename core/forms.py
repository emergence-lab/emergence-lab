from django import forms
from django.core.exceptions import ValidationError

from .models import project, investigation, project_tracking


class CreateInvestigationForm(forms.ModelForm):

    class Meta:
        model = investigation
        fields = ('name', 'description')


class TrackProjectForm(forms.ModelForm):

    def save(self, **kwargs):
        commit = kwargs.pop('commit', True)
        operator = kwargs.pop('operator')

        instance = super(TrackProjectForm, self).save(commit=False)
        instance.operator = operator

        if commit:
            instance.save()

        return instance

    class Meta:
        model = project_tracking
        fields = ['project', 'is_pi']
