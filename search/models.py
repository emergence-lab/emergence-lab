from django.conf import settings

from elasticsearch_dsl import DocType, String, Date

from .utils import html_strip


class Document(DocType):
    created = Date()

    def get_index_name(self):
        return self._get_index()


class Process(Document):
    title = String(analyzer='snowball')
    comment = String(analyzer=html_strip,
                     fields={'raw': String(index='not_analyzed')})
    process_type = String(analyzer='snowball')
    legacy_identifier = String(index='not_analyzed')
    uuid = String(index='not_analyzed')

    class Meta:
        index = '{}processes'.format(settings.ELASTICSEARCH_PREFIX)


class Sample(Document):
    comment = String(analyzer=html_strip,
                     fields={'raw': String(index='not_analyzed')})
    uuid = String(index='not_analyzed')

    class Meta:
        index = '{}samples'.format(settings.ELASTICSEARCH_PREFIX)
