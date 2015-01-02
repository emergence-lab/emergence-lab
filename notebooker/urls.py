from django.conf.urls import patterns, url
from notebooker import views
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    #url(r'^new/$', login_required(views.ReservationCreate.as_view()), name='reservation_create'),
    #url(r'^edit/(?P<pk>\d+)/$', login_required(views.ReservationEdit.as_view()), name='reservation_edit'),
    #url(r'^cancel/(?P<pk>\d+)/$', login_required(never_cache(views.CancelReservation.as_view())), name='cancel_reservation'),
    #url(r'^close/(?P<pk>\d+)/$', login_required(never_cache(views.CloseReservation.as_view())), name='close_reservation'),
    #url(r'^increase/(?P<pk>\d+)/$', login_required(never_cache(views.IncreasePriority.as_view())), name='increase_priority'),
    #url(r'^decrease/(?P<pk>\d+)/$', login_required(never_cache(views.DecreasePriority.as_view())), name='decrease_priority'),
    #url(r'^(?P<tool_slug>[a-z0-9\-]+)/$', login_required(never_cache(views.ReservationListByTool.as_view())), name='reservation_list_by_tool'),
    url(r'^edit/(?P<notebook_name>[a-z0-9\w-]+)/(?P<cell>\d+)$', login_required(views.CellEdit.as_view()), name='notebook_cell_edit'),
    url(r'^inttest/(?P<notebook_name>[a-z0-9\w-]+)$', login_required(views.NotebookIntDemo.as_view()), name='notebook_int_demo'),

    url(r'^test/(?P<notebook_name>[a-z0-9\w-]+)$', login_required(views.NotebookDemo.as_view()), name='notebook_demo'),

    url(r'^$', login_required(views.NotebookList.as_view()), name='notebook_list'),
)
