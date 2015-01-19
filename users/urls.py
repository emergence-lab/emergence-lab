from django.conf.urls import patterns, url
from users import views
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^users/(?P<username>[\w-]+)/add_git_token$', login_required(views._GetGitLabToken.as_view()), name='git_token_form'),
    url(r'^users/(?P<username>[\w-]+)$', login_required(views.UserProfile.as_view()), name='users_profile')
)
