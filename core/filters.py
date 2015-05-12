# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import operator

from django import forms
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from datetimewidget.widgets import DateWidget
import django_filters

from core.models import Sample, Process
from d180.models import D180Growth
from core.polymorphic import get_subclasses


def _filter_process_type(queryset, value):
    if not value:
        return queryset

    classes = [Process.get_process_class(slug) for slug in value]
    return queryset.by_process_types(classes, combine_and=False)


def _filter_d180_growth_tags(queryset, value):
    if not value:
        return queryset

    growth_ctype = ContentType.objects.get_for_model(D180Growth).id

    for sample in queryset:
        d180_process_ids = (sample.nodes.order_by()
                                        .exclude(process_id__isnull=True)
                                        .filter(process__polymorphic_ctype=growth_ctype)
                                        .values_list('process_id', flat=True)
                                        .distinct())
        d180_processes = D180Growth.objects.filter(id__in=d180_process_ids)
        filter_args = []
        for v in value:
            tmp = {}
            tmp[v] = True
            filter_args.append(tmp)
        q_filters = [Q(**arg) for arg in filter_args]
        d180_processes = d180_processes.filter(reduce(operator.and_, q_filters))
        if not d180_processes.exists():
            queryset = queryset.exclude(id=sample.id)
    return queryset


def _filter_process_user(queryset, value):
    if not value:
        return queryset

    return queryset.filter_process(user_id=value)


def _filter_process_comment(queryset, value):
    if not value:
        return queryset

    return queryset.filter_process(comment__icontains=value)


class SampleFilterSet(django_filters.FilterSet):
    D180_TAGS_CHOICES = [
        ('has_gan', 'Has GaN'),
        ('has_aln', 'Has AlN'),
        ('has_inn', 'Has InN'),
        ('has_algan', 'Has AlGaN'),
        ('has_ingan', 'Has InGaN'),
        ('has_u', 'Has Undoped Material'),
        ('has_n', 'Has N-type Material'),
        ('has_p', 'Has P-type Material'),
        ('is_template', 'Is Template'),
        ('is_buffer', 'Is Buffer'),
        ('has_pulsed', 'Has Pulsed Layer(s)'),
        ('has_graded', 'Has Graded Layer(s)'),
        ('has_superlattice', 'Has Superlattice Layers'),
        ('has_mqw', 'Has MQW Layers'),
    ]

    created = django_filters.DateFilter(
        lookup_type=['exact', 'lt', 'lte', 'gt', 'gte'],
        widget=DateWidget(
            attrs={'class': 'datetime'},
            bootstrap_version=3,
            options={'minView': '2',
                     'startView': '2',
                     'todayBtn': 'true',
                     'todayHighlight': 'true',
                     'clearBtn': 'true',
                     'format': 'yyyy-mm-dd'}))
    modified = django_filters.DateFilter(
        lookup_type=['exact', 'lt', 'lte', 'gt', 'gte'],
        widget=DateWidget(
            attrs={'class': 'datetime'},
            bootstrap_version=3,
            options={'minView': '2',
                     'startView': '2',
                     'todayBtn': 'true',
                     'todayHighlight': 'true',
                     'clearBtn': 'true',
                     'format': 'yyyy-mm-dd'}))
    d180_tags = django_filters.MultipleChoiceFilter(
        choices=D180_TAGS_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        label='D180 Tags',
        action=_filter_d180_growth_tags
        )
    process_comment = django_filters.CharFilter(
        label='Process Comment',
        action=_filter_process_comment
        )

    def __init__(self, *args, **kwargs):
        super(SampleFilterSet, self).__init__(*args, **kwargs)

        process_types = get_subclasses(Process) + [Process]
        self.filters['process_type'] = django_filters.MultipleChoiceFilter(
            choices=[(p.slug, p.name) for p in process_types],
            action=_filter_process_type)
        users = [(u.id, u.get_full_name())
                 for u in get_user_model().active_objects.all()]
        self.filters['process_user'] = django_filters.ChoiceFilter(
            choices=[('', 'Any User')] + users,
            action=_filter_process_user)

    class Meta:
        model = Sample
        order_by = ('-created', 'created', '-modified', 'modified', 'uuid')
        fields = ('created', 'modified', 'd180_tags', 'process_comment')
