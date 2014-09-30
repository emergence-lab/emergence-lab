from django import forms

from .models import journal_entry


class JournalEntryForm(forms.ModelForm):

    class Meta:
        model = journal_entry
        fields = ('title', 'entry', 'investigations')
