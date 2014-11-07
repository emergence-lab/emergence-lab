import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (CreateView, DetailView, ListView,
                                  RedirectView, TemplateView, View, UpdateView)

from braces.views import LoginRequiredMixin
import gitlab

from .models import Investigation, operator, Project, project_tracking
from growths.models import growth, sample
from .forms import TrackProjectForm
from .streams import (project_stream, investigation_stream,
                      operator_investigation_stream)
from journal.models import journal_entry


##############
# Misc Views #
##############

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
                                token=settings.GITLAB_PRIVATE_TOKEN, verify_ssl=False)
            success = git.createissue(8, title=title, labels=', '.join(tags),
                                      description='User: {0}\n\nPage: {1}\n\nProblem: {2}'.format(user, path, complaint))
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


class ActivateOperatorRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified operator to active.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.pop('id')
        operator_obj = operator.objects.get(pk=pk)
        operator_obj.activate()
        return reverse('operator_list')


class DeactivateOperatorRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified operator to inactive.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.pop('id')
        operator_obj = operator.objects.get(pk=pk)
        operator_obj.deactivate()
        return reverse('operator_list')


class ProjectListView(LoginRequiredMixin, ActiveListView):
    """
    View to list all projects and provide actions.
    """
    template_name = "core/project_list.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['tracking'] = project_tracking.objects.filter(operator=self.request.user.operator).values_list('project_id', flat=True)
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """
    View for details of a project.
    """
    template_name = 'core/project_detail.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        if 'username' in self.kwargs:
            userid = operator.objects.filter(user__username=self.kwargs['username']).values('id')
            context['growths'] = (growth.objects.filter(project=self.object,
                                                        operator_id=userid)
                                                .order_by('-growth_number')[:25])
            context['entries'] = (journal_entry.objects.filter(investigations__in=self.object.investigation_set.all(),
                                                               author_id=userid)
                                                        .order_by('-date')[:25])
            context['tracking'] = (project_tracking.objects.filter(operator_id=userid,
                                                                   project=self.object)
                                                           .exists())
        else:
            context['growths'] = (growth.objects.filter(project=self.object)
                                                .order_by('-growth_number')[:25])
            context['entries'] = (journal_entry.objects.filter(investigations__in=self.object.investigation_set.all())
                                                       .order_by('-date')[:25])
            context['tracking'] = (project_tracking.objects.filter(operator=self.request.user.operator,
                                                                   project=self.object)
                                                           .exists())
        context['stream'] = project_stream(self.object)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a project.
    """
    template_name = 'core/project_create.html'
    model = Project
    fields = ('name', 'description',)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('project_detail_all', kwargs={'slug': self.object.slug})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for editing information about a project.
    """
    template_name = 'core/project_update.html'
    model = Project
    fields = ('description',)

    def get_success_url(self):
        return reverse('project_detail_all', kwargs={'slug': self.object.slug})


class TrackProjectRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified project as tracked for the logged in user.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.pop('slug')
        project = Project.objects.get(slug=slug)
        operator_obj = self.request.user.operator
        tracking_obj, created = project_tracking.objects.get_or_create(project=project,
                                                                       operator=operator_obj,
                                                                       defaults={'is_pi': False})
        return reverse('project_list')


class UntrackProjectRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified project as not tracked for the logged in user.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.pop('slug')
        project_obj = Project.objects.get(slug=slug)
        operator_obj = self.request.user.operator
        tracking_obj = project_tracking.objects.filter(project=project_obj,
                                                       operator=operator_obj)
        if tracking_obj.count():
            tracking_obj.delete()
        return reverse('project_list')


class ActivateProjectRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified project to active.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.pop('slug')
        project = Project.objects.get(slug=slug)
        project.activate()
        return reverse('project_list')


class DeactivateProjectRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified project to inactive.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.pop('slug')
        project = Project.objects.get(slug=slug)
        project.deactivate()
        return reverse('project_list')


class InvestigationDetailView(LoginRequiredMixin, DetailView):
    """
    View for details of an investigation.
    """
    template_name = 'core/investigation_detail.html'
    model = Investigation

    def get_context_data(self, **kwargs):
        context = super(InvestigationDetailView, self).get_context_data(**kwargs)
        if 'username' in self.kwargs:
            userid = operator.objects.filter(user__username=self.kwargs['username']).values('id')
            context['growths'] = (growth.objects.filter(project=self.object,
                                                        operator_id=userid)
                                                .order_by('-growth_number')[:25])
            context['entries'] = (journal_entry.objects.filter(investigations__pk=self.object.id,
                                                               author_id=userid)
                                                       .order_by('-date')[:25])
            context['stream'] = operator_investigation_stream(userid, self.object)
        else:
            context['growths'] = (growth.objects.filter(project=self.object)
                                                .order_by('-growth_number')[:25])
            context['entries'] = (journal_entry.objects.filter(investigations__pk=self.object.id)
                                                       .order_by('-date')[:25])
            context['stream'] = investigation_stream(self.object)
        context['project'] = self.object.project
        return context


class InvestigationCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating an investigation.
    """
    template_name = 'core/investigation_create.html'
    model = Investigation
    fields = ('name', 'description')

    def dispatch(self, request, *args, **kwargs):
        self.initial = {'project': Project.objects.get(slug=kwargs.pop('slug'))}
        return super(InvestigationCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.project = self.initial['project']
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('investigation_detail_all', kwargs={'project': self.object.project.slug,
                                                           'slug': self.object.slug})


class InvestigationUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for editing information about a project.
    """
    template_name = 'core/investigation_update.html'
    model = Investigation
    fields = ('description',)

    def get_success_url(self):
        return reverse('investigation_detail_all', kwargs={'project': self.object.project.slug,
                                                           'slug': self.object.slug})


class InvestigationListView(LoginRequiredMixin, ActiveListView):
    """
    View to list all projects and provide actions.
    """
    template_name = "core/investigation_list.html"
    model = Investigation


class ActivateInvestigationRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified investigation to active.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.pop('slug')
        investigation = Investigation.objects.get(slug=slug)
        investigation.activate()
        return reverse('project_list')


class DeactivateInvestigationRedirectView(LoginRequiredMixin, RedirectView):
    """
    Sets the specified investigation to inactive.
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.pop('slug')
        investigation = Investigation.objects.get(slug=slug)
        investigation.deactivate()
        return reverse('project_list')


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
            self.object.is_pi = form.cleaned_data['is_pi']
            self.object.save()
        except:
            self.object = form.save(operator=self.request.user.operator)
        return HttpResponseRedirect(reverse('dashboard'))
