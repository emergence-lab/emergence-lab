# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models

import uuidfield


class RichTextField(models.TextField):
    """
    Field to handle rich text with the hallojs editor.
    """
    pass


class UUIDField(uuidfield.UUIDField):
    """
    Passthrough to allow Django 1.7 migrations
    """
    def deconstruct(self):
        return models.Field.deconstruct(self)