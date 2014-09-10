from django import forms
from django.core.exceptions import ValidationError

from core.forms import MarkdownField
from .models import journal_entry


class JournalEntryForm(forms.ModelForm):
    entry = MarkdownField()

    class Meta:
        model = journal_entry
        fields = ('title', 'entry', 'investigations')
