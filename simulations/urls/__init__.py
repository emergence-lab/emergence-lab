from django.conf.urls import url

from simulations import views


urlpatterns = [
    url(r'^$', views.SimulationAdmin.as_view(), name='simulation_admin'),
    url(r'^start_instance/(?P<instance_id>[a-z0-9\-]+)$',
        views.StartInstance.as_view(), name='start_instance'),
    url(r'^stop_instance/(?P<instance_id>[a-z0-9\-]+)$',
        views.StopInstance.as_view(), name='stop_instance'),
]
