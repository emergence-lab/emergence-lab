import os

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView, RedirectView, TemplateView, View, FormView

import gitlab
from actstream import action

from .models import investigation, operator, platter, project, project_tracking
from growths.models import growth, sample
from .forms import TrackProjectForm


class SessionHistoryMixin(object):
    max_history = 5
    request = None

    def add_breadcrumb_history(self, request):
        history = request.session.get('breadcrumb_history', [])

        if not history or history[-1] != request.path:
            history.append(request.path)

        if len(history) > self.max_history:
            history.pop(0)

        request.session['breadcrumb_history'] = history
        return history

    def get_context_data(self, **kwargs):
        kwargs['breadcrumb'] = self.add_breadcrumb_history(self.request)
        return super(SessionHistoryMixin, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(SessionHistoryMixin, self).dispatch(request, *args, **kwargs)


class ActiveListView(ListView):
    """
    View to handle models using the active and inactive manager.
    """
    def get_context_data(self, **kwargs):
        context = super(ActiveListView, self).get_context_data(**kwargs)
        context['active_list'] = self.model.current.all()
        context['inactive_list'] = self.model.retired.all()
        return context


class QuickSearchRedirect(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        growth_number = self.request.GET.get('growth', None)
        try:
            growth.get_growth(growth_number)
            return reverse('growth_detail', args=(growth_number,))
        except:
            try:
                obj = sample.get_sample(growth_number)
                return reverse('sample_detail', args=(obj.id,))
            except:
                pass
        return reverse('afm_filter')


class homepage(TemplateView):
    """
    View for the homepage of the application.
    """
    template_name = "core/index.html"


def protected_media(request, filename):
    fullpath = os.path.join(settings.MEDIA_ROOT, filename)
    response = HttpResponse(mimetype='image/jpeg')
    response['X-Sendfile'] = fullpath
    return response


class operator_list(ActiveListView):
    """
    View to list all operators and provide actions.
    """
    template_name = "core/operator_list.html"
    model = operator


class operator_create(CreateView):
    """
    View to create operators.
    """
    template_name = "core/operator_create.html"
    model = operator
    fields = ['name']

    def get_success_url(self):
        return reverse('operator_list')


class platter_list(ActiveListView):
    """
    View to list all operators and provide actions.
    """
    template_name = "core/platter_list.html"
    model = platter


class ProjectDetailView(DetailView):
    """
    View for details of a project.
    """
    template_name = 'core/project_detail.html'
    model = project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        if 'username' in self.kwargs:
            userid = operator.objects.filter(user__username=self.kwargs['username']).values('id')
            context['growths'] = (growth.objects.filter(project=self.object,
                                                        operator_id=userid)
                                                .order_by('-growth_number')[:25])
        else:
            context['growths'] = (growth.objects.filter(project=self.object)
                                                .order_by('-growth_number')[:25])
        return context


class InvestigationDetailView(DetailView):
    """
    View for details of an investigation.
    """
    template_name = 'core/investigation_detail.html'
    model = investigation

    def get_context_data(self, **kwargs):
        context = super(InvestigationDetailView, self).get_context_data(**kwargs)
        if 'username' in self.kwargs:
            userid = operator.objects.filter(user__username=self.kwargs['username']).values('id')
            context['growths'] = (growth.objects.filter(project=self.object,
                                                        operator_id=userid)
                                                .order_by('-growth_number')[:25])
        else:
            context['growths'] = (growth.objects.filter(project=self.object)
                                                .order_by('-growth_number')[:25])
        context['project'] = self.object.project
        return context


class project_list(ActiveListView):
    """
    View to list all projects and provide actions.
    """
    template_name = "core/project_list.html"
    model = project


class investigation_list(ActiveListView):
    """
    View to list all projects and provide actions.
    """
    template_name = "core/investigation_list.html"
    model = investigation


class ExceptionHandlerView(View):

    def post(self, request, *args, **kwargs):
        path = request.POST.get('path', '')
        user = request.POST.get('user', 0)
        title = request.POST.get('title', 'Exception Form Issue')
        tags = request.POST.getlist('tag[]')
        tags.append('exception-form')
        complaint = request.POST.get('complaint', '')
        if complaint:
            git = gitlab.Gitlab(settings.GITLAB_HOST,
                                token=settings.GITLAB_PRIVATE_TOKEN, verify_ssl=False)
            success = git.createissue(8, title=title, labels=', '.join(tags),
                                      description='User: {0}\nPage: {1}\nProblem: {2}'.format(user, path, complaint))
            if not success:
                raise Exception('Error submitting issue')
        return HttpResponseRedirect(path)


class TrackProjectView(CreateView):
    model = project_tracking
    form_class = TrackProjectForm
    template_name = 'core/track_project.html'

    def form_valid(self, form):
        project_id = form.cleaned_data['project']
        try:
            self.object = project_tracking.objects.get(operator=self.request.user.operator, project_id=project_id)
            if self.object.is_pi != form.cleaned_data['is_pi']:
                if form.cleaned_data['is_pi']:
                    verb = 'added as owner of'
                else:
                    verb = 'removed as owner of'
            else:
                verb = None
            self.object.is_pi = form.cleaned_data['is_pi']
            self.object.save()
        except:
            self.object = form.save(operator=self.request.user.operator)
            if form.cleaned_data['is_pi']:
                verb = 'added as owner of'
            else:
                verb = 'started watching'
        if verb:
            action.send(self.request.user.operator, verb=verb, target=project_id)
        return HttpResponseRedirect(reverse('dashboard'))
