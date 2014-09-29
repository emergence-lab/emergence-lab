from django.apps import AppConfig
from django.contrib.auth import get_user_model

from actstream import registry


class CoreAppConfig(AppConfig):
    name = 'core'

    def ready(self):
        registry.register(self.get_model('project'))
        registry.register(self.get_model('investigation'))
        registry.register(self.get_model('operator'))
        registry.register(get_user_model())
