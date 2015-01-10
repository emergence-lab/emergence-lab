from django.shortcuts import render
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from django.views.generic import ListView, RedirectView, TemplateView, FormView
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings

import gitlab
from users.forms import GitTokenForm

User = get_user_model()

# Create your views here.

class UserProfile(TemplateView):
    template_name = 'users/profile_view.html'

    def get_context_data(self, **kwargs):
        if 'thisuser' not in kwargs:
            kwargs['thisuser'] = User.objects.get(username=kwargs['username'])
        return super(UserProfile, self).get_context_data(**kwargs)

class _GetGitLabToken(FormView):
    template_name = 'users/gitlab_get_token_form.html'
    form_class = GitTokenForm

    def get_initial(self):
        initial = super(_GetGitLabToken, self).get_initial()
        initial['user'] = str(self.request.user)
        return initial

    #def get_context_data(self, **kwargs):
    #    if 'thisuser' not in kwargs:
    #        kwargs['thisuser'] = kwargs['username']
    #    return super(UserProfile, self).get_context_data(**kwargs)

    def form_valid(self, form):
        git = gitlab.Gitlab(settings.GITLAB_HOST, verify_ssl=False)
        #try:
        git.login(form.cleaned_data['user'], form.cleaned_data['password'])
        tmp = git.currentuser()
        user.gitlab_token = tmp['private_token']
        user.gitlab_id = tmp['id']
        #except Exception as e: print e
        return HttpResponseRedirect(reverse('users_profile', kwargs={'username': str(self.request.user)}))
