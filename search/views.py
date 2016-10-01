from django.conf import settings
from django.views import generic

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

from braces.views import LoginRequiredMixin


client = Elasticsearch([settings.ELASTICSEARCH_HOST])


class ElasticSearchView(LoginRequiredMixin, generic.TemplateView):

    template_name = "search/basic_search.html"

    def build_query(self, search_query):
        search_type = self.request.GET.get('type')

        if search_type not in ['processes', 'samples']:
            search_type = "processes"

        search_bool_shoulds = [
            Q("match", comment=search_query),
            Q("match", uuid=search_query),
        ]

        if search_type == "processes":
            search_bool_shoulds.append(Q("match", title=search_query))
            search_bool_shoulds.append(Q("match",
                                         legacy_identifier=search_query))

        return search_type, search_bool_shoulds

    def get_context_data(self, **kwargs):
        context = super(ElasticSearchView, self).get_context_data(**kwargs)

        search_query = self.request.GET.get('query', '')

        index, shoulds = self.build_query(search_query)

        query_object = Q("bool",
                         should=shoulds,
                         minimum_should_match=1)

        search_query = Search(
            using=client,
            index=index
        ).query(query_object).sort("-created")

        context['search_query'] = search_query.execute().hits

        return context
