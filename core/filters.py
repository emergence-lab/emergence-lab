# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import operator

from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model

from datetimewidget.widgets import DateWidget
import django_filters

from core.models import Sample, ProcessType


def _filter_process_type(queryset, value):
    if not value:
        return queryset

    return queryset.by_process_types(value, combine_and=False)


def _filter_d180_growth_tags(queryset, value):
    if not value:
        return queryset

    filter_args = ({'process__info__{}'.format(v): True} for v in value)
    q_filters = (Q(**arg) for arg in filter_args)

    return queryset.filter_process(reduce(operator.and_, q_filters))


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
        ('Material', (
            ('has_gan', 'Has GaN'),
            ('has_aln', 'Has AlN'),
            ('has_inn', 'Has InN'),
            ('has_algan', 'Has AlGaN'),
            ('has_ingan', 'Has InGaN'),
        )),
        ('Doping', (
            ('has_u', 'Has Undoped Material'),
            ('has_n', 'Has N-type Material'),
            ('has_p', 'Has P-type Material'),
        )),
        ('Growth Features', (
            ('is_template', 'Is Template'),
            ('is_buffer', 'Is Buffer'),
            ('has_pulsed', 'Has Pulsed Layer(s)'),
            ('has_graded', 'Has Graded Layer(s)'),
            ('has_superlattice', 'Has Superlattice Layers'),
            ('has_mqw', 'Has MQW Layers'),
        )),
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
        widget=forms.SelectMultiple(),
        label='D180 Tags',
        action=_filter_d180_growth_tags
        )
    process_comment = django_filters.CharFilter(
        label='Process Comment',
        action=_filter_process_comment
        )

    def __init__(self, *args, **kwargs):
        super(SampleFilterSet, self).__init__(*args, **kwargs)

        self.filters['process_type'] = django_filters.MultipleChoiceFilter(
            choices=[(p.type, p.name) for p in ProcessType.objects.all()],
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
