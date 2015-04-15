# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig

from actstream import registry


class JournalAppConfig(AppConfig):
    name = 'journal'

    def ready(self):
        registry.register(self.get_model('JournalEntry'))
