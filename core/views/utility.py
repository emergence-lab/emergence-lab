# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import subprocess

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.cache import add_never_cache_headers
from django.views import generic

from braces.views import LoginRequiredMixin
import gitlab
from sendfile import sendfile

from core.models import Process, Sample


class NeverCacheMixin(object):
    """
    Mixin to ensure the results of requests are never cached.
    Class-based alternative to django.views.decorators.never_cache
    """

    def dispatch(self, request, *args, **kwargs):
        response = super(NeverCacheMixin, self).dispatch(request, *args, **kwargs)
        add_never_cache_headers(response)
        return response


class ActionReloadView(NeverCacheMixin, generic.RedirectView):
    """
    View to perform an action and reload the page.
    """
    permanent = False

    def perform_action(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        self.perform_action(request, *args, **kwargs)
        return super(ActionReloadView, self).get(request, *args, **kwargs)


class ActiveListView(generic.ListView):
    """
    View to handle models using the active and inactive manager.
    """
    def get_context_data(self, **kwargs):
        context = super(ActiveListView, self).get_context_data(**kwargs)
        context['active_list'] = self.model.active_objects.all()
        context['inactive_list'] = self.model.inactive_objects.all()
        return context


class ProtectedMediaView(LoginRequiredMixin, generic.View):
    """
    Allows media files to be protected via Django authentication
    """

    def get(self, request, filename, *args, **kwargs):
        return sendfile(request, os.path.join(settings.MEDIA_ROOT, filename))


class ExceptionHandlerView(LoginRequiredMixin, generic.View):
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


class QuickSearchRedirectView(LoginRequiredMixin, generic.RedirectView):
    """
    View to handle redirection to the correct growth or sample from the
    quicksearch bar in the page header.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        query = self.request.GET.get('search_query', '')
        if query.startswith('s'):
            try:
                sample = Sample.objects.get_by_uuid(query)
                return reverse('sample_detail', args=(sample.uuid,))
            except Sample.DoesNotExist:
                return reverse('sample_list')
        elif query.startswith('p'):
            try:
                uuid = Process.strip_uuid(query)
                process = Process.objects.get(uuid_full__startswith=uuid)
                return reverse('process_detail', args=(process.uuid,))
            except Process.DoesNotExist:
                return reverse('process_list')
        elif query.startswith('@'):
            return reverse('users_profile',
                           kwargs={'username': query.strip('@')})
        else:
            try:
                process = Process.objects.get(legacy_identifier=query)
                return reverse('process_detail', args=(process.uuid,))
            except Process.DoesNotExist:
                return reverse('sample_search')


class HomepageView(generic.TemplateView):
    """
    View for the homepage of the application.
    """
    template_name = "core/index.html"


class AboutView(generic.TemplateView):
    """
    View to show information about running build of the code.
    """
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        try:
            branch = subprocess.check_output(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=settings.BASE_DIR).strip()
            commit = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                cwd=settings.BASE_DIR).strip()
            tag = subprocess.check_output(
                ['git', 'describe', '--tags'],
                cwd=settings.BASE_DIR).strip()
        except subprocess.CalledProcessError as e:
            raise e
            context['error'] = '{0}: {1}'.format(e.returncode,
                                                 e.output)
            return context
        context['tag'] = tag
        context['commit'] = commit[:7]
        context['branch'] = branch
        return context
