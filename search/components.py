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
    index_name = None

    def create_index(self):
        self.search_model.init()

    def delete_index(self):
        index = Index(self.index_name)
        index.delete(ignore=404)

    def close_index(self):
        index = Index(self.index_name)
        index.close(ignore=404)

    def index_all(self):
        items = self.object_model.objects.all()

        for item in items:
            self.index_item(item)

    def reindex_all(self):
        self.delete_index()
        self.create_index()
        self.index_all()

    def delete_item(self, id):
        item = self.search_model.get(id)
        item.delete()


class ProcessSearchComponent(SearchComponent):

    search_model = Process()
    object_model = ProcessModel
    index_name = "{}processes".format(settings.ELASTICSEARCH_PREFIX)

    def index_item(self, process):

        process_meta = {'id': process.id}

        process_document = Process(
            title=process.title,
            comment=process.comment,
            process_type=process.type.name,
            legacy_identifier=process.legacy_identifier,
            uuid=process.uuid,
            created=process.created,
            meta=process_meta
        )

        process_document.save()


class SampleSearchComponent(SearchComponent):

    search_model = Sample()
    object_model = SampleModel
    index_name = "{}samples".format(settings.ELASTICSEARCH_PREFIX)

    def index_item(self, process):

        process_meta = {'id': process.id}

        process_document = Sample(
            comment=process.comment,
            uuid=process.uuid_full,
            created=process.created,
            meta=process_meta
        )

        process_document.save()
