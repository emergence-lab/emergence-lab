from django.shortcuts import render
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from django.views.generic import ListView, RedirectView, TemplateView, FormView
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class UserProfile(TemplateView):
    template_name = 'users/profile_view.html'

    def get_context_data(self, **kwargs):
        if 'thisuser' not in kwargs:
            kwargs['thisuser'] = User.objects.get(username=kwargs['username'])
        return super(UserProfile, self).get_context_data(**kwargs)
