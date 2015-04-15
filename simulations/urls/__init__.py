from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from simulations import views


urlpatterns = [
    url(r'^$', login_required(never_cache(views.SimulationAdmin.as_view())), name='simulation_admin'),
    url(r'^start_instance/(?P<instance_id>[a-z0-9\-]+)$', staff_member_required(never_cache(views.StartInstance.as_view())), name='start_instance'),
    url(r'^stop_instance/(?P<instance_id>[a-z0-9\-]+)$', staff_member_required(never_cache(views.StopInstance.as_view())), name='stop_instance'),
]
