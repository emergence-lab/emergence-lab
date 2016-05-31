# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models

from core.configuration.fields import ConfigurationField
from core.configuration.models import ConfigurationManager


class ConfigurationTestModel(models.Model):

    configuration = ConfigurationField()

    objects = ConfigurationManager()
