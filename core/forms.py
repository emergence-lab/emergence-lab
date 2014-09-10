from django import forms
from django.core.exceptions import ValidationError

from html2text import html2text
from ckeditor.widgets import CKEditorWidget

from .models import project, investigation, project_tracking


class MarkdownField(forms.CharField):
    widget = CKEditorWidget()

    def clean(self, value):
        value = super(MarkdownField, self).clean(value)
        try:
            return html2text(value)
        except:
            raise ValidationError


class CreateProjectForm(forms.ModelForm):
    description = MarkdownField()

    class Meta:
        model = project
        fields = ('name', 'description')


class CreateInvestigationForm(forms.ModelForm):
    description = MarkdownField()

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
