# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, RedirectView, TemplateView, View

from braces.views import LoginRequiredMixin
import gitlab


class ActiveListView(ListView):
    """
    View to handle models using the active and inactive manager.
    """
    def get_context_data(self, **kwargs):
        context = super(ActiveListView, self).get_context_data(**kwargs)
        context['active_list'] = self.model.active_objects.all()
        context['inactive_list'] = self.model.inactive_objects.all()
        return context


@login_required
def protected_media(request, filename):
    """
    Allows media files to be protected via Django authentication
    """
    fullpath = os.path.join(settings.MEDIA_ROOT, filename)
    response = HttpResponse(mimetype='image/jpeg')
    response['X-Sendfile'] = fullpath
    return response


class ExceptionHandlerView(LoginRequiredMixin, View):
    """
    Handles creating an exception via ajax.
    """
    def post(self, request, *args, **kwargs):
        path = request.POST.get('path', '')
        user = request.POST.get('user', 0)
        title = request.POST.get('title', 'Exception Form Issue')
        tags = request.POST.getlist('tag[]')
        tags.append('exception-form')
        complaint = request.POST.get('complaint', '')
        if complaint:
            git = gitlab.Gitlab(settings.GITLAB_HOST,
                                token=settings.GITLAB_PRIVATE_TOKEN,
                                verify_ssl=False)
            description = ('User: {}\n'
                           'Page: {}\n'
                           'Problem: {}'.format(user, path, complaint))
            success = git.createissue(8, title=title, labels=', '.join(tags),
                                      description=description)
            if not success:
                raise Exception('Error submitting issue')
        return HttpResponseRedirect(path)


class QuickSearchRedirectView(LoginRequiredMixin, RedirectView):
    """
    View to handle redirection to the correct growth or sample from the
    quicksearch bar in the page header.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse('home')


class HomepageView(TemplateView):
    """
    View for the homepage of the application.
    """
    template_name = "core/index.html"
