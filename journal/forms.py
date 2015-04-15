# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from .models import JournalEntry


class JournalEntryForm(forms.ModelForm):

    class Meta:
        model = JournalEntry
        fields = ('title', 'entry', 'investigations')
