from elasticsearch_dsl import Index
from elasticsearch_dsl.connections import connections

from core.models import Process as ProcessModel
from core.models import Sample as SampleModel
from .models import Process, Sample

from django.conf import settings


# Define a default Elasticsearch client
connections.create_connection(hosts=[settings.ELASTICSEARCH_HOST])


class SearchComponent(object):

    search_model = None
    object_model = None

    def create_index(self):
        self.search_model.init()

    def delete_index(self):
        index = Index(self.search_model.get_index_name())
        index.delete(ignore=404)

    def index_all(self):
        items = self.object_model.objects.all()

        for item in items:
            self.index_item(item)

    def reindex_all(self):
        self.delete_index()
        self.create_index()
        self.index_all()


class ProcessComponent(SearchComponent):

    search_model = Process()
    object_model = ProcessModel

    def index_item(self, process):

        process_meta = {'id': process.id}

        process_document = Process(
            title=process.title,
            comment=process.comment,
            process_type=process.type.name,
            legacy_identifier=process.legacy_identifier,
            uuid_full=process.uuid_full,
            created=process.created,
            meta=process_meta
        )

        process_document.save()


class SampleComponent(SearchComponent):

    search_model = Sample()
    object_model = SampleModel

    def index_item(self, process):

        process_meta = {'id': process.id}

        process_document = Sample(
            comment=process.comment,
            uuid_full=process.uuid_full,
            created=process.created,
            meta=process_meta
        )

        process_document.save()
