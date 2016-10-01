from django.core.management.base import BaseCommand

from search.components import ProcessComponent, SampleComponent


class Command(BaseCommand):

    def handle(self, *args, **options):
        ProcessComponent().reindex_all()
        SampleComponent().reindex_all()
