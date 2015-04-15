# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from afm.models import AFMScan
from core.forms import AutoCreateForm


class AutoCreateAFMForm(AutoCreateForm):

    class Meta:
        model = AFMScan
        fields = ('comment',)
