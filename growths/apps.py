from django.apps import AppConfig

from actstream import registry


class GrowthsAppConfig(AppConfig):
    name = 'growths'

    def ready(self):
        registry.register(self.get_model('growth'))
        registry.register(self.get_model('sample'))
