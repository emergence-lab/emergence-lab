from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.views.generic import (TemplateView, FormView, UpdateView,
                                  CreateView, ListView)
from django.contrib.auth import get_user_model
from django.conf import settings
from redis import StrictRedis
import pickle

import gitlab
from rest_framework.authtoken.models import Token
from braces.views import LoginRequiredMixin, UserPassesTestMixin, StaffuserRequiredMixin

from core.forms import CreateUserForm, EditUserForm
from users.forms import GitTokenForm
from users.redis_config import GitCredential

User = get_user_model()


class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile_view.html'

    def get_context_data(self, **kwargs):
        if 'thisuser' not in kwargs:
            kwargs['thisuser'] = User.objects.get(username=kwargs['username'])
            r = StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)
            try:
                kwargs['thisuser'].em_token = Token.objects.get(
                    user=User.objects.get(username=kwargs['username']))
                kwargs['thisuser'].gitlab_token = pickle.loads(
                    r.get('users:{0}:git.credential'.format(
                        kwargs['thisuser'].id))).token
                kwargs['thisuser'].gitlab_id = pickle.loads(
                    r.get('users:{0}:git.credential'.format(
                        kwargs['thisuser'].id))).gitlab_id
            except TypeError:
                pass
        return super(UserProfile, self).get_context_data(**kwargs)


class UserUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'users/user_edit.html'
    form_class = EditUserForm
    lookup_url_kwarg = 'username'

    def test_func(self, user):
        return (user.username == self.kwargs.get('username') or user.is_staff)

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset
        username = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(User, username=username)

    def get_success_url(self):
        if self.request.user == self.object:
            return reverse('users_profile', args=(self.request.user.username,))
        else:
            return reverse('user_list')


class UserCreateView(StaffuserRequiredMixin, CreateView):
    template_name = 'users/user_create.html'
    form_class = CreateUserForm

    def get_success_url(self):
        return reverse('user_list')


class UserListView(StaffuserRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    paginate_by = 20


class _GetGitLabToken(LoginRequiredMixin, FormView):
    template_name = 'users/gitlab_get_token_form.html'
    form_class = GitTokenForm

    def get_initial(self):
        initial = super(_GetGitLabToken, self).get_initial()
        initial['user'] = str(self.request.user)
        return initial

    def form_valid(self, form):
        git = gitlab.Gitlab(settings.GITLAB_HOST, verify_ssl=False)
        try:
            g = GitCredential()
            r = StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)
            git.login(form.cleaned_data['user'], form.cleaned_data['password'])
            tmp = git.currentuser()
            g.token = tmp['private_token']
            g.gitlab_id = tmp['id']
            r.set('users:{0}:git.credential'.format(self.request.user.id), pickle.dumps(g))
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse('users_profile',
                                            kwargs={'username': str(self.request.user)}))
