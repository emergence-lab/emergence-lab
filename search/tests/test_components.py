# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from time import sleep

from django.conf import settings
from django.test import TestCase

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index, Search, Q

from model_mommy import mommy

from core.models import Process as ProcessModel
from core.models import Sample as SampleModel
from search.components import ProcessSearchComponent, SampleSearchComponent
from search.models import Process, Sample


client = Elasticsearch([settings.ELASTICSEARCH_HOST])


class BaseSearchTestClass(TestCase):

    model = None
    search_model = None
    search_component = None
#
    def __init__( self, *args, **kwargs ):
        super(BaseSearchTestClass, self).__init__( *args, **kwargs )
        self.helper = None
        # This is to prevent the base class from being run
        if self.__class__ != BaseSearchTestClass:
            # Rebind `run' from the parent class.
            self.run = TestCase.run.__get__( self, self.__class__ )
        else:
            self.run = lambda self, *args, **kwargs: None

    def get_all_indexed_documents(self):
        return self.build_query(Q("match_all"))

    def build_query(self, query_object):

        search_query = Search(
            using=client,
            index=self.search_component().index_name
        ).query(query_object).sort("-created")

        return search_query.execute().hits

    def test_all_the_things(self):
        # All in one test because otherwise there are index errors
        self.search_component().delete_index()
        self.search_component().create_index()

        self.assertEqual(len(self.get_all_indexed_documents()), 0)

        for idx in range(3):
            mommy.make(self.model)

        self.search_component().index_all()

        # This is because Elasticsearch needs a second to crawl the documents
        sleep(1)

        self.assertEqual(len(self.model.objects.all()), 3)
        self.assertEqual(len(self.get_all_indexed_documents()), 3)

        mommy.make(self.model)

        # Same as above
        sleep(1)

        self.assertEqual(len(self.model.objects.all()), 4)
        self.assertEqual(len(self.get_all_indexed_documents()), 4)

        # Cleanup
        self.search_component().delete_index()


class TestProcessSearchComponent(BaseSearchTestClass):

    model = ProcessModel
    search_model = Process
    search_component = ProcessSearchComponent


class TestSampleSearchComponent(BaseSearchTestClass):
    model = SampleModel
    search_model = Sample
    search_component = SampleSearchComponent
