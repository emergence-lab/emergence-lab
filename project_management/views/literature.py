# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from time import sleep
import os

from django.core.urlresolvers import reverse
from django.views import generic
from django.conf import settings
from django.http import HttpResponseRedirect

from braces.views import LoginRequiredMixin
from mendeley import Mendeley
from mendeley.session import MendeleySession
from mendeley.exception import MendeleyApiException
from oauthlib.oauth2 import TokenExpiredError

from core.views import ActionReloadView
from core.models import Investigation, Milestone
from project_management.models import Literature


def pagination_helper(page, count, queryset):
    if page and int(page) > 1 and int(page) <= count / 10:
        number = int(page) - 1
        for i in range(0, number):
            queryset = queryset.next_page
    return queryset


class MendeleyMixin(object):

    def get(self, request, *args, **kwargs):
        if 'token' in request.session:
            try:
                self.mendeley = Mendeley(settings.MENDELEY_ID,
                                            settings.MENDELEY_SECRET,
                                            settings.MENDELEY_REDIRECT)
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
        mendeley = Mendeley(settings.MENDELEY_ID,
                            settings.MENDELEY_SECRET,
                            settings.MENDELEY_REDIRECT)
        self.auth = mendeley.start_authorization_code_flow(request.session.get('state', ''))
        if 'state' not in request.session:
            request.session['state'] = self.auth.state
            print(request.session['state'])
        try:
            # print(request.get_full_path())
            # print(request.session['state'])
            if not settings.MENDELEY_SSL_VERIFY:
                os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
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
            return reverse('mendeley_search')


class LiteratureListView(LoginRequiredMixin, MendeleyMixin, generic.TemplateView):

    template_name = 'project_management/literature_list.html'

    def get_context_data(self, **kwargs):
        page = self.request.GET.get('page', None)
        context = super(LiteratureListView, self).get_context_data(**kwargs)
        literature = self.session.documents.list(page_size=10, view='tags')
        # literature = session.documents.search('Basic').list()
        context['literature'] = pagination_helper(page, literature.count, literature)
        context['milestones'] = Milestone.objects.all().filter(user=self.request.user)
        context['investigations'] = Investigation.objects.all().filter(is_active=True)
        return context


class MendeleyLibrarySearchView(LoginRequiredMixin, MendeleyMixin, generic.TemplateView):

    template_name = 'project_management/mendeley_search.html'

    def get_context_data(self, **kwargs):
        page = self.request.GET.get('page', None)
        query = str(self.request.GET.get('query', None))
        context = super(MendeleyLibrarySearchView, self).get_context_data(**kwargs)
        try:
            literature = self.session.documents.search(query).list()
        except MendeleyApiException:
            try:
                sleep(1)
                literature = self.session.documents.search(query).list()
            except:
                raise
        context['literature'] = pagination_helper(page, literature.count, literature)
        context['milestones'] = Milestone.objects.all().filter(user=self.request.user)
        context['investigations'] = Investigation.objects.all().filter(is_active=True)
        return context


class LiteratureRedirectorView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        if settings.ENABLE_MENDELEY:
            return reverse('mendeley_search')
        else:
            return reverse('literature_landing')


class LiteratureLandingView(LoginRequiredMixin, generic.ListView):

    template_name = 'project_management/literature_landing.html'
    model = Literature
    paginate_by = 25

    def get_queryset(self):
        queryset = super(LiteratureLandingView, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(LiteratureLandingView, self).get_context_data(**kwargs)
        context['mendeley'] = settings.ENABLE_MENDELEY
        context['milestones'] = Milestone.objects.all().filter(user=self.request.user)
        context['investigations'] = Investigation.objects.all().filter(is_active=True)
        return context


class AddMendeleyObjectView(LoginRequiredMixin, MendeleyMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        tmp = Literature.objects.all().filter(external_id=self.kwargs['external_id'])
        if tmp.filter(user=self.request.user).exists():
            obj = tmp.filter(user=self.request.user).first()
            if 'milestone' in self.kwargs and Milestone.objects.get(
                    id=self.kwargs['milestone']) not in obj.milestones.all():
                obj.milestones.add(Milestone.objects.get(id=self.kwargs['milestone']))
            if 'investigation' in self.kwargs and Investigation.objects.get(
                    id=self.kwargs['investigation']) not in obj.investigations.all():
                obj.investigations.add(Investigation.objects.get(id=self.kwargs['investigation']))
            obj.save()
        else:
            document = self.session.documents.get(self.kwargs.get('external_id', None))
            external_id = getattr(document, 'id', None)
            title = unicode(getattr(document, 'title', None))
            journal = getattr(document, 'journal', None)
            year = getattr(document, 'year', None)
            abstract = getattr(document, 'abstract', None)
            if document.identifiers and document.identifiers.get('doi', None):
                doi_number = document.identifiers.get('doi', None)
            else:
                doi_number = None
            user = self.request.user
            literature = Literature.objects.create(external_id=external_id, title=title,
                                                    journal=journal, year=year, abstract=abstract,
                                                    doi_number=doi_number, user=user)
            if 'milestone' in self.kwargs:
                literature.milestones.add(Milestone.objects.get(id=self.kwargs['milestone']))
            if 'investigation' in self.kwargs:
                literature.investigations.add(Investigation.objects.get(
                    id=self.kwargs['investigation']))
            literature.save()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('literature_landing')


class AddLiteratureObjectView(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        literature = Literature.objects.all().get(id=self.kwargs.pk)
        if 'milestone' in self.kwargs:
            milestone = Milestone.objects.get(id=self.kwargs['milestone'])
            if milestone not in literature.milestones:
                literature.milestones.add(milestone)
        if 'investigation' in self.kwargs:
            investigation = Investigation.objects.get(id=self.kwargs['investigation'])
            if milestone not in literature.milestones:
                literature.investigations.add(investigation)
        literature.save()

    def get_redirect_url(self, *args, **kwargs):
        return reverse('literature_landing')


class CreateLiteratureObjectView(LoginRequiredMixin, generic.CreateView):

    model = Literature
    template_name = 'project_management/create_literature.html'


class LiteratureDetailRedirector(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        literature = Literature.objects.get(id=self.kwargs['pk'])
        if literature.user == self.request.user:
            if literature.external_id:
                return reverse('mendeley_detail', kwargs={'external_id': literature.external_id})
            else:
                return reverse('literature_detail', kwargs={'pk': literature.id})
        else:
            return reverse('literature_landing')


class LiteratureDetailView(LoginRequiredMixin, generic.DetailView):

    model = Literature
    template_name = 'project_management/literature_detail.html'


class MendeleyDetailView(LoginRequiredMixin, MendeleyMixin, generic.TemplateView):

    template_name = 'project_management/literature_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MendeleyDetailView, self).get_context_data(**kwargs)
        context['literature'] = self.session.documents.get(self.kwargs['external_id'])
        print(context['literature'].title)
        return context
