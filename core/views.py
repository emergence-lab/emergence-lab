import os

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView, RedirectView, TemplateView, View, FormView
from django.contrib.auth.decorators import login_required

import gitlab
from actstream import action
from braces.views import LoginRequiredMixin

from .models import investigation, operator, platter, project, project_tracking
from growths.models import growth, sample
from .forms import TrackProjectForm
from .streams import project_stream, operator_project_stream, investigation_stream, operator_investigation_stream


##############
# Misc Views #
##############

class ActiveListView(ListView):
    """
    View to handle models using the active and inactive manager.
    """
    def get_context_data(self, **kwargs):
        context = super(ActiveListView, self).get_context_data(**kwargs)
        context['active_list'] = self.model.current.all()
        context['inactive_list'] = self.model.retired.all()
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
                                token=settings.GITLAB_PRIVATE_TOKEN, verify_ssl=False)
            success = git.createissue(8, title=title, labels=', '.join(tags),
                                      description='User: {0}\nPage: {1}\nProblem: {2}'.format(user, path, complaint))
            if not success:
                raise Exception('Error submitting issue')
        return HttpResponseRedirect(path)


class QuickSearchRedirectView(LoginRequiredMixin, RedirectView):
    """
    View to handle redirection to the correct growth or sample from the
    quicksearch bar in the page header.
    """
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


class HomepageView(TemplateView):
    """
    View for the homepage of the application.
    """
    template_name = "core/index.html"


###############
# Model Views #
###############

class OperatorListView(LoginRequiredMixin, ActiveListView):
    """
    View to list all operators and provide actions.
    """
    template_name = "core/operator_list.html"
    model = operator


class PlatterListView(LoginRequiredMixin, ActiveListView):
    """
    View to list all operators and provide actions.
    """
    template_name = "core/platter_list.html"
    model = platter


class ProjectListView(LoginRequiredMixin, ActiveListView):
    """
    View to list all projects and provide actions.
    """
    template_name = "core/project_list.html"
    model = project

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['tracking'] = project_tracking.objects.filter(operator=self.request.user.operator).values_list('project_id', flat=True)
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
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
        context['stream'] = project_stream(self.object)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a project.
    """
    template_name = 'core/project_create.html'
    model = project
    fields = ('name', 'description')

    def form_valid(self, form):
        self.object = form.save()
        action.send(self.request.user.operator, verb='created', target=self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('project_detail_all', kwargs={'slug': self.object.slug})


class InvestigationDetailView(LoginRequiredMixin, DetailView):
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
            context['stream'] = operator_investigation_stream(userid, self.object)
        else:
            context['growths'] = (growth.objects.filter(project=self.object)
                                                .order_by('-growth_number')[:25])
            context['stream'] = investigation_stream(self.object)
        context['project'] = self.object.project
        return context


class InvestigationCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating an investigation.
    """
    template_name = 'core/investigation_create.html'
    model = investigation
    fields = ('name', 'description')

    def dispatch(self, request, *args, **kwargs):
        print(kwargs)
        self.initial = {'project': project.objects.get(slug=kwargs.pop('slug'))}
        return super(InvestigationCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.project = self.initial['project']
        self.object = form.save()
        action.send(self.request.user.operator, verb='added investigation to',
                    target=self.object.project, investigation=self.object.id)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('investigation_detail_all', kwargs={'project': self.object.project.slug,
                                                           'slug': self.object.slug})


class InvestigationListView(LoginRequiredMixin, ActiveListView):
    """
    View to list all projects and provide actions.
    """
    template_name = "core/investigation_list.html"
    model = investigation


class TrackProjectView(LoginRequiredMixin, CreateView):
    """
    View to handle tracking projects.
    """
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
