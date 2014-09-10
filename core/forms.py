from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from html2text import html2text
from ckeditor.widgets import CKEditorWidget

from .models import project_tracking


class MarkdownField(forms.CharField):
    widget = CKEditorWidget()

    def clean(self, value):
        value = super(MarkdownField, self).clean(value)
        try:
            return html2text(value)
        except:
            raise ValidationError


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
