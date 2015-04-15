# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from sem.models import SEMScan
from core.forms import AutoCreateForm


class AutoCreateSEMForm(AutoCreateForm):

    class Meta:
        model = SEMScan
        fields = ('comment',)
