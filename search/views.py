from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.cache import add_never_cache_headers
from django.views import generic

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

from braces.views import LoginRequiredMixin


client = Elasticsearch([settings.ELASTICSEARCH_HOST])


class ElasticSearchView(LoginRequiredMixin, generic.TemplateView):

    template_name = "search/basic_search.html"

    def build_query(self, query):
        search_type = self.request.GET.get('type')

        if not search_type in ['processes', 'samples']:
            search_type = "processes"

        search_bool_shoulds = [
            Q("match", comment=query),
            Q("match", uuid_full=query),
        ]

        if search_type == "processes":
            search_bool_shoulds.append(Q("match", title=query))
            search_bool_shoulds.append(Q("match", legacy_identifier=query))

        return search_type, search_bool_shoulds

    def get_context_data(self, **kwargs):
        context = super(ElasticSearchView, self).get_context_data(**kwargs)

        query = self.request.GET.get('query', '')

        index, shoulds = self.build_query(query)

        query_object = Q("bool",
                         should=shoulds,
                         minimum_should_match=1)

        search_query = Search(using=client, index=index).query(query_object)

        context['search_query'] = search_query.execute().hits

        return context
