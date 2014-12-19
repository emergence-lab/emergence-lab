from django import forms

from .models import ProjectTracking


class TrackProjectForm(forms.ModelForm):

    def save(self, **kwargs):
        commit = kwargs.pop('commit', True)
        user = kwargs.pop('user')

        instance = super(TrackProjectForm, self).save(commit=False)
        instance.user = user

        if commit:
            instance.save()

        return instance

    class Meta:
        model = ProjectTracking
        fields = ['project', 'is_owner']


class ChecklistForm(forms.Form):
    checklist_fields = []

    def __init__(self, *args, **kwargs):
        super(ChecklistForm, self).__init__(*args, **kwargs)
        for i, label in enumerate(self.checklist_fields):
            self.fields['field_{0}'.format(i)] = forms.BooleanField(required=True, label=label)
