# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import functools
import operator

from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model

import django_filters

from core.models import Sample, ProcessType
from core.utils import DateWidget, DATE_LOOKUP_CHOICES, EnhancedDateFilter


def _filter_process_type(queryset, name, value):
    if not value:
        return queryset

    return queryset.by_process_types(value, combine_and=False)


def _filter_d180_growth_tags(queryset, name, value):
    if not value:
        return queryset

    filter_args = ({'process__info__{}'.format(v): True} for v in value)
    q_filters = (Q(**arg) for arg in filter_args)

    return queryset.filter_process(functools.reduce(operator.and_, q_filters))


def _filter_process_user(queryset, name, value):
    if not value:
        return queryset

    return queryset.filter_process(user_id=value)


def _filter_process_comment(queryset, name, value):
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

    created = EnhancedDateFilter(
        # lookup_expr=['exact', 'lt', 'lte', 'gt', 'gte'],
        lookup_choices=DATE_LOOKUP_CHOICES,
        widget=DateWidget(
            attrs={'class': 'datetime'},
            bootstrap_version=3,
            options={'todayBtn': 'true',
                     'todayHighlight': 'true',
                     'clearBtn': 'true',
                     'format': 'yyyy-mm-dd'}))
    modified = EnhancedDateFilter(
        # lookup_expr=['exact', 'lt', 'lte', 'gt', 'gte'],
        lookup_choices=DATE_LOOKUP_CHOICES,
        widget=DateWidget(
            attrs={'class': 'datetime'},
            bootstrap_version=3,
            options={'todayBtn': 'true',
                     'todayHighlight': 'true',
                     'clearBtn': 'true',
                     'format': 'yyyy-mm-dd'}))
    d180_tags = django_filters.MultipleChoiceFilter(
        choices=D180_TAGS_CHOICES,
        widget=forms.SelectMultiple(),
        label='D180 Tags',
        method=_filter_d180_growth_tags
        )
    process_comment = django_filters.CharFilter(
        label='Process Comment',
        method=_filter_process_comment
        )
    ordering = django_filters.OrderingFilter(
        fields=(
            ('created', 'created'),
            ('modified', 'modified'),
            ('id', 'uuid'),
        ),
        field_labels={
            'uuid': 'UUID',
        },
    )

    def __init__(self, *args, **kwargs):
        super(SampleFilterSet, self).__init__(*args, **kwargs)

        self.filters['process_type'] = django_filters.MultipleChoiceFilter(
            choices=[(p.type, p.name) for p in ProcessType.objects.all()],
            method=_filter_process_type)
        users = [(u.id, u.get_full_name())
                 for u in get_user_model().active_objects.all()]
        self.filters['process_user'] = django_filters.ChoiceFilter(
            choices=[('', 'Any User')] + users,
            method=_filter_process_user)

    class Meta:
        model = Sample
        fields = ('ordering', 'created', 'modified', 'd180_tags', 'process_comment')
