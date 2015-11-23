from django.conf.urls import patterns, url
from users import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^users/(?P<username>[\w-]+)/add_git_token$',
        login_required(views._GetGitLabToken.as_view()),
        name='git_token_form'),
    url(r'^users/detail/(?P<username>[\w-]+)$',
        login_required(views.UserProfile.as_view()),
        name='users_profile'),
    url(r'^users/edit/(?P<username>[\w-]+)$',
        login_required(views.UserUpdateView.as_view()),
        name='user_edit'),
    url(r'^users/list$',
        login_required(views.UserListView.as_view()),
        name='user_list'),
    url(r'^users/create$',
        login_required(views.UserCreateView.as_view()),
        name='user_create')
)
