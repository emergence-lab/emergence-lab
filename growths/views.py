from django.shortcuts import render
from django.views.generic import DetailView, ListView, FormView
from django_filters import FilterSet, CharFilter, NumberFilter, Filter, BooleanFilter
from django_filters.views import FilterView
from django.shortcuts import render_to_response
from django import forms

import sys

from core.models import afm, growth


# TODO: don't hardcode names as <model>__<field>, get name from FilterSet class
class RelationalFilterView(FilterView):
    def get(self, request, *args, **kwargs):
        filterset_class = self.get_filterset_class()
        self.filterset = self.get_filterset(filterset_class)
        self.object_list = self.filterset.qs

        # TODO: clean this up since it is still pretty messy
        # for each object (i.e. growth) loop through each declared relational_field
        #   for each relational field, get the parameters from GET and filter the dataset on it
        #   put the final result in <model>_filter context parameter
        # you can still use <model>_set.all for a nonfiltered list
        for obj in self.object_list:
            for model, fields in self.filterset.Meta.relational_fields.iteritems():
                qs = getattr(obj, model + "_set").all()
                prefix = model + '__'
                # filter for '<model>__' in GET
                get_params = list(k for k,v in request.GET.iteritems() if prefix in k)
                for field in fields:
                    # sort by final character (#)
                    final_params = sorted(list(v for v in get_params if field in v), key=lambda str:str[-1])
                    if final_params:
                        # TODO: break this out into relational_action parameter?
                        # TODO: add relationalfilter to auto-handle naming etc?
                        value = request.GET.get(final_params[0])
                        lookup = request.GET.get(final_params[1])
                        if value:
                            qs = qs.filter(**{field + '__' + lookup: value})
                setattr(obj, model + "_filter", qs)

        context = self.get_context_data(filter=self.filterset, object_list=self.object_list)
        return self.render_to_response(context)


class growth_filter(FilterSet):
    operator = CharFilter(lookup_type='icontains')
    project = CharFilter(lookup_type='icontains')
    layeris_uid = BooleanFilter()
    afm__rms = NumberFilter(lookup_type=['exact', 'lt', 'lte', 'gt', 'gte'], distinct=True)
    afm__zrange = NumberFilter(lookup_type=['exact', 'lt', 'lte', 'gt', 'gte'], distinct=True)
    afm__size = NumberFilter(lookup_type=['exact', 'lt', 'lte', 'gt', 'gte'], distinct=True)

    # TODO: break this out into RelationalFilterSet class
    def __init__(self, *args, **kwargs):
        # add relational_fields to fields with <model>__<field>
        for k,v in self.Meta.relational_fields.iteritems():
            for r in v:
                self.Meta.fields.append(k + '__' + r)
        super(growth_filter, self).__init__(*args, **kwargs)

    class Meta:
        model = growth
        fields = ['growth_number', 'operator', 'project','layeris_uid']
        relational_fields = {
            'afm': ['rms', 'zrange', 'size'],
        }
        order_by = ['growth_number']


class growth_list(RelationalFilterView):
    filterset_class = growth_filter
    template_name = 'core/growth_filter.html'


class growth_detail(DetailView):
    model = growth
    template_name = 'core/growth_detail.html'
    slug_field = 'growth_number'


class afm_detail(DetailView):
    model = afm
    template_name = 'core/afm_detail.html'
