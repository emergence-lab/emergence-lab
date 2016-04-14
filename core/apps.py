# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig
from django.contrib.auth import get_user_model



class CoreAppConfig(AppConfig):
    name = 'core'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Project'))
        registry.register(self.get_model('Investigation'))
        registry.register(self.get_model('Process'))
        registry.register(get_user_model())
