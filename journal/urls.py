from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^create/$', views.JournalCreateView.as_view(), name='journal_create'),
    url(r'^(?P<username>[\w-]+)/$', views.JournalListView.as_view(), name='journal_list'),
    url(r'^(?P<username>[\w-]+)/(?P<slug>[\w-]+)/', views.JournalDetailView.as_view(), name='journal_detail'),
]
