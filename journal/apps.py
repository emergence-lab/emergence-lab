# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig



class JournalAppConfig(AppConfig):
    name = 'journal'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('JournalEntry'))
