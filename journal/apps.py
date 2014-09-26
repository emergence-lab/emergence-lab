from django.apps import AppConfig

from actstream import registry


class JournalAppConfig(AppConfig):
    name = 'journal'

    def ready(self):
        registry.register(self.get_model('journal_entry'))
