# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from .mixins import TimestampMixin
from .process import get_process_choices


@python_2_unicode_compatible
class SampleNode(MPTTModel, TimestampMixin):
    uid = models.SlugField(max_length=20)
    comment = models.TextField(blank=True)
    parent = TreeForeignKey('self', null=True, related_name='children')
    content_type = models.ForeignKey(ContentType, null=True,
        limit_choices_to=get_process_choices())
    object_id = models.PositiveIntegerField(null=True)
    process = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.uid
