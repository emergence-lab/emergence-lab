# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from django import template
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse


register = template.Library()


def create_process_link(match):
    s = match.group(0).split('#')[-1]
    try:
        link = reverse('process_detail', kwargs={'uuid': s})
    except Exception:
        link = '#'
    return '<a href="{0}">{1}</a>'.format(link, s)


def create_sample_link(match):
    s = match.group(0).split('#')[-1]
    try:
        link = reverse('sample_detail', kwargs={'uuid': s})
    except Exception:
        link = '#'
    return '<a href="{0}">{1}</a>'.format(link, s)


def create_literature_link(match):
    s = match.group(0).split('#lit-')[-1]
    try:
        link = reverse('literature_detail_redirector', kwargs={'pk': s})
    except Exception:
        link = '#'
    return '<a href="{0}">literature_{1}</a>'.format(link, s)


def convert_to_links(update):

    # links samples
    update = re.sub(r"#s\w+", create_sample_link, update)

    # links processes
    update = re.sub(r"#p\w+", create_process_link, update)

    # links literature
    update = re.sub(r"#lit-\w+", create_literature_link, update)

    return mark_safe(update)

convert_to_links.is_safe = True
register.filter('convert_to_links', convert_to_links)
