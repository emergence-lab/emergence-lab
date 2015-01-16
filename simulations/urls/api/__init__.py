# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from simulations import api


urlpatterns = [
    url(r'^$', api.SimulationListAPIView.as_view()),
    #url(r'^(?P<pk>[0-9]+)/$', api.SimulationRetrieveAPIView.as_view()),
    #url(r'^(?P<pk>[0-9]+)/update/$', api.SimulationUpdateAPIView.as_view()),
    #url(r'^(?P<pk>[0-9]+)/cancel/$', api.SimulationDestroyAPIView.as_view()),
    #url(r'^/running/$', api.RunningSimulationListAPIView.as_view()),
    #url(r'^/completed/$', api.CompletedSimulationListAPIView.as_view()),
    #url(r'^/queue/$', api.QueueListCreateAPIView.as_view()),
    #url(r'^/queue/next/$', api.NextSimulationRetrieveAPIView.as_view()),
    #url(r'^/queue/nodes/$', api.NodesListAPIView.as_view()),
    # url(r'^/queue/nodes/(?P<instance_type>.+)/$',
    #     api.NodeQueueListAPIView.as_view()),
    # url(r'^/queue/nodes/(?P<instance_type>.+)/next/$',
    #     api.NextSimulationNodesRetrieveAPIView.as_view()),
    # url(r'^/queue/priorities/$', api.PrioritiesListAPIView.as_view()),
    # url(r'^/queue/priorities/(?P<priority_type>.+)/$',
    #     api.PriorityQueueListAPIView.as_view()),
    # url(r'^/queue/priorities/(?P<priority_type>.+)/next/$',
    #     api.NextSimulationPriorityRetrieveAPIView.as_view()),
]
