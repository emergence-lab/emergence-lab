# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms


class ChecklistForm(forms.Form):
    checklist_fields = []

    def __init__(self, *args, **kwargs):
        super(ChecklistForm, self).__init__(*args, **kwargs)
        for i, label in enumerate(self.checklist_fields):
            self.fields['field_{}'.format(i)] = forms.BooleanField(required=True,
                                                                   label=label)
