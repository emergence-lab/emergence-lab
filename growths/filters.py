import sys

import django_filters as filters
from django_filters.views import FilterView
from datetimewidget.widgets import DateTimeWidget
from django import forms

from core.models import operator, project, investigation
from growths.models import growth
from afm.models import afm


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
                get_params = list(k for k, v in request.GET.iteritems() if prefix in k)
                for field in fields:  # <model>__<field>
                    # sort by final character (#)
                    final_params = sorted(list(v for v in get_params if field in v), key=lambda str: str[-1])
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


class growth_filter(filters.FilterSet):
    operator = filters.ModelMultipleChoiceFilter(queryset=operator.objects.filter(active=True))
    project = filters.ModelMultipleChoiceFilter(queryset=project.objects.all())
    investigation = filters.ModelMultipleChoiceFilter(queryset=investigation.objects.all())
    date = filters.DateFilter(lookup_type=['exact', 'lt', 'lte', 'gt', 'gte'],
                              widget=DateTimeWidget(attrs={'class': 'datetime'},
                                                    options={'minView': '2',
                                                             'startView': '3',
                                                             'todayBtn': 'true',
                                                             'clearBtn': 'true',
                                                             'format': 'yyyy-mm-dd'}))
    afm__rms = filters.NumberFilter(lookup_type=['exact', 'lt', 'lte', 'gt', 'gte'], distinct=True)
    afm__zrange = filters.NumberFilter(lookup_type=['exact', 'lt', 'lte', 'gt', 'gte'], distinct=True)
    afm__size = filters.NumberFilter(lookup_type=['exact', 'lt', 'lte', 'gt', 'gte'], distinct=True)
    hall__sheet_concentration = filters.NumberFilter(lookup_type=['exact', 'lt', 'lte', 'gt', 'gte'], distinct=True)
    hall__sheet_resistance = filters.NumberFilter(lookup_type=['exact', 'lt', 'lte', 'gt', 'gte'], distinct=True)
    hall__mobility = filters.NumberFilter(lookup_type=['exact', 'lt', 'lte', 'gt', 'gte'], distinct=True)
    hall__bulk_concentration = filters.NumberFilter(lookup_type=['exact', 'lt', 'lte', 'gt', 'gte'], distinct=True)
    hall__bulk_resistance = filters.NumberFilter(lookup_type=['exact', 'lt', 'lte', 'gt', 'gte'], distinct=True)

    # TODO: break this out into RelationalFilterSet class
    def __init__(self, *args, **kwargs):
        # add relational_fields to fields with <model>__<field>
        for k, v in self.Meta.relational_fields.iteritems():
            for r in v:
                self.Meta.fields.append(k + '__' + r)
        super(growth_filter, self).__init__(*args, **kwargs)

    class Meta:
        model = growth
        fields = ['growth_number', 'date', 'operator', 'project', 'investigation', 'platter',
                  'reactor', 'has_n', 'has_p', 'has_u', 'has_gan', 'has_algan', 'has_aln',
                  'is_template', 'is_buffer', 'has_graded', 'has_superlattice', 'has_mqw', ]
        relational_fields = {
            'afm': ['rms', 'zrange', 'size'],
            'hall': ['sheet_concentration', 'sheet_resistance', 'mobility', 'bulk_concentration', 'bulk_resistance']
        }
        order_by = ['-growth_number']
