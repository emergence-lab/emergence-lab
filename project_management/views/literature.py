# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic
from django.conf import settings
from django.http import HttpResponseRedirect

from braces.views import LoginRequiredMixin
from mendeley import Mendeley
from mendeley.session import MendeleySession
from oauthlib.oauth2 import TokenExpiredError

from core.views import ActionReloadView
from core.models import Investigation
from project_management.models import Literature, Milestone


def pagination_helper(page, count, queryset):
    if page and int(page) > 1 and int(page) <= count/10 :
        number = int(page) - 1
        for i in range(0,number):
            queryset = queryset.next_page
    return queryset


class MendeleyMixin(object):

    def get(self, request, *args, **kwargs):
        if 'token' in request.session:
            try:
                self.mendeley = Mendeley(settings.MENDELEY_ID, settings.MENDELEY_SECRET, 'http://localhost:8000/oauth')
                self.session = MendeleySession(self.mendeley, request.session['token'])
                return super(MendeleyMixin, self).get(request, *args, **kwargs)
            except TokenExpiredError:
                print('TOKEN_EXPIRED')
                request.session.pop('token')
                return HttpResponseRedirect(reverse('mendeley_oauth'))
        else:
            return HttpResponseRedirect(reverse('mendeley_oauth'))


class MendeleyOAuth(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        mendeley = Mendeley(settings.MENDELEY_ID, settings.MENDELEY_SECRET, 'http://localhost:8000/oauth')
        self.auth = mendeley.start_authorization_code_flow(request.session.get('state', ''))
        if 'state' not in request.session:
            request.session['state'] = self.auth.state
            print(request.session['state'])
        try:
            print(request.get_full_path())
            print(request.session['state'])
            mendeley_session = self.auth.authenticate(request.get_full_path())
            request.session['token'] = mendeley_session.token
            # self.session['state'] = self.auth.state
            # print(self.kwargs['state'])
        except Exception as e:
            print(self.auth.get_login_url())
            print(e)
            pass

    def get_redirect_url(self, *args, **kwargs):
        if 'token' not in self.request.session:
            return self.auth.get_login_url()
        else:
            return reverse('literature_list')


class LiteratureListView(LoginRequiredMixin, MendeleyMixin, generic.TemplateView):

    template_name = 'project_management/literature_list.html'

    def get_context_data(self, **kwargs):
        page = self.request.GET.get('page', None)
        context = super(LiteratureListView, self).get_context_data(**kwargs)
        literature = self.session.documents.list(page_size=10,view='tags')
        # literature = session.documents.search('Basic').list()
        count = literature.count
        if page and int(page) > 1 and int(page) <= count/10 :
            number = int(page) - 1
            # literature = session.documents.list(page_size=10,view='client')
            for i in range(0,number):
                literature = literature.next_page
        context['literature'] = literature
        return context


class MendeleyLibrarySearchView(LoginRequiredMixin, MendeleyMixin, generic.TemplateView):

    template_name = 'project_management/mendeley_search.html'

    def get_context_data(self, **kwargs):
        page = self.request.GET.get('page', None)
        query = str(self.request.GET.get('query', None))
        context = super(MendeleyLibrarySearchView, self).get_context_data(**kwargs)
        # literature = self.session.documents.list(page_size=10,view='tags')
        literature = self.session.documents.search(query).list()
        # literature = pagination_helper(page, count, self.session.documents.search(query).list())
        # if page and int(page) > 1 and int(page) <= count/10 :
        #     number = int(page) - 1
        #     for i in range(0,number):
        #         literature = literature.next_page
        context['literature'] = pagination_helper(page, literature.count, literature)
        return context


class LiteratureLandingView(LoginRequiredMixin, generic.ListView):

    template_name = 'project_management/literature_landing.html'
    model = Literature

    def get_queryset(self):
        queryset = super(LiteratureLandingView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class AddMendeleyObjectView(LoginRequiredMixin, MendeleyMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        if not Literature.objects.filter(
                user=self.request.user).filter(external_id=self.kwargs['external_id']).exists():
            document = self.session.documents.get(self.kwargs['external_id'])
            literature = Literature.objects.create(external_id=document.id,
                                                    title=document.title,
                                                    journal=document.source,
                                                    year=document.year,
                                                    abstract=document.abstract,
                                                    doi_number=document.identifiers.get('doi',
                                                                                        None),
                                                    user=self.request.user)
            if 'milestone' in self.kwargs:
                literature.milestones.add(Milestone.objects.get(id=self.kwargs['milestone']))
            if 'investigation' in self.kwargs:
                literature.investigations.add(Investigation.objects.get(id=self.kwargs['investigation']))

    def get_redirect_url(self, *args, **kwargs):
        return reverse('literature_list')
