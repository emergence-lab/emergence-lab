from django.core.management.base import BaseCommand

from search.components import ProcessSearchComponent, SampleSearchComponent


class Command(BaseCommand):

    def handle(self, *args, **options):
        ProcessSearchComponent().reindex_all()
        SampleSearchComponent().reindex_all()
