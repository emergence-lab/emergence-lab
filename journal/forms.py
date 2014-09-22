from django import forms
from django.core.exceptions import ValidationError

from .models import journal_entry


class JournalEntryForm(forms.ModelForm):

    class Meta:
        model = journal_entry
        fields = ('title', 'entry', 'investigations')
