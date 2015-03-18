from django.conf.urls import patterns, url
from notebooker import views
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^view/(?P<notebook_name>[a-z0-9\w-]+)$',
        login_required(views.NotebookViewer.as_view()),
        name='notebook_viewer'),
    url(r'^$', login_required(views.NotebookList.as_view()),
        name='notebook_list'),
)
