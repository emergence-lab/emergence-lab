from django.conf.urls import patterns, url
from schedule_queue import views
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^new/$',
        login_required(views.ReservationCreate.as_view()),
        name='reservation_create'),
    url(r'^edit/(?P<pk>\d+)/$',
        login_required(views.ReservationEdit.as_view()),
        name='reservation_edit'),
    url(r'^cancel/(?P<pk>\d+)/$',
        login_required(never_cache(views.CancelReservation.as_view())),
        name='cancel_reservation'),
    url(r'^close/(?P<pk>\d+)/$',
        login_required(never_cache(views.CloseReservation.as_view())),
        name='close_reservation'),
    url(r'^increase/(?P<pk>\d+)/$',
        login_required(never_cache(views.IncreasePriority.as_view())),
        name='increase_priority'),
    url(r'^decrease/(?P<pk>\d+)/$',
        login_required(never_cache(views.DecreasePriority.as_view())),
        name='decrease_priority'),
    url(r'^(?P<tool_slug>[a-z0-9\-]+)/$',
        login_required(never_cache(views.ReservationListByTool.as_view())),
        name='reservation_list_by_tool'),
    url(r'^$', views.ReservationLanding.as_view(),
        name='reservation_landing'),
)
