# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings


def external_links(request):
    """
    Add external links to context for all views for use in header bar.
    """
    external_links = settings.EXTERNAL_LINKS or {}
    return {'external_links': external_links}


def feedback(request):
    """
    Add feedback form for reporting bugs.
    """
    feedback = settings.ENABLE_FEEDBACK or False
    return {'feedback': feedback}
