from datetime import datetime
from elasticsearch_dsl import DocType, String, Date, Integer

from .utils import html_strip


class Document(DocType):
    created = Date()

    def get_index_name(self):
        return self._get_index()


class Process(Document):
    title = String(analyzer='snowball')
    comment = String(analyzer=html_strip, fields={'raw': String(index='not_analyzed')})
    process_type = String(analyzer='snowball')
    legacy_identifier = String(index='not_analyzed')
    uuid_full = String(index='not_analyzed')

    class Meta:
        index = 'processes'


class Sample(Document):
    comment = String(analyzer=html_strip, fields={'raw': String(index='not_analyzed')})
    uuid_full = String(index='not_analyzed')

    class Meta:
        index = 'samples'
