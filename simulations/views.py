# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import reverse
from django.conf import settings
from django.views.generic import TemplateView

import aws_support as aws
from braces.views import LoginRequiredMixin

from core.views import ActionReloadView, NeverCacheMixin


class StartInstance(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        signals = aws.EC2Connection(settings.AWS_EC2_REGION,
                                    settings.AWS_ACCESS_KEY_ID,
                                    settings.AWS_SECRET_ACCESS_KEY)
        instance = kwargs.pop('instance_id')
        try:
            signals.start_instance(instance)
        except Exception as e:
            raise Exception(e)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('simulation_admin')


class StopInstance(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        signals = aws.EC2Connection(settings.AWS_EC2_REGION,
                                    settings.AWS_ACCESS_KEY_ID,
                                    settings.AWS_SECRET_ACCESS_KEY)
        instance = kwargs.pop('instance_id')
        try:
            signals.stop_instance(instance)
        except Exception as e:
            raise Exception(e)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('simulation_admin')


class SimulationAdmin(LoginRequiredMixin, NeverCacheMixin, TemplateView):
    template_name = 'simulations/admin.html'

    signals = aws.EC2Connection(settings.AWS_EC2_REGION,
                                settings.AWS_ACCESS_KEY_ID,
                                settings.AWS_SECRET_ACCESS_KEY)

    def get_context_data(self, **kwargs):
        tmp = []
        if 'instances' not in kwargs:
            for instance in self.signals.instance_list():
                tmp.append({'instance_name': instance.id,
                            'instance_address': instance.ip_address,
                            'instance_type': instance.instance_type,
                            'instance_state': instance.state,
                            'instance_uptime': self.signals.instance_uptime(instance.id)})
            kwargs['instances'] = tmp
        return super(SimulationAdmin, self).get_context_data(**kwargs)
