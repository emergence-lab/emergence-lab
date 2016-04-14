# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django import forms


class RichTextField(models.TextField):
    """
    Field to handle rich text with the hallojs editor.
    """
    def formfield(self, **kwargs):
        kwargs.update({
            'widget': forms.Textarea(attrs={'class': 'hallo'})})
        return super(RichTextField, self).formfield(**kwargs)
