from django import forms
from django.forms import ModelForm

from .models import project_tracking


class TrackProjectForm(ModelForm):

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
