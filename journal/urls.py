from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^create/$', views.JournalCreateView.as_view(), name='journal_create'),
)
