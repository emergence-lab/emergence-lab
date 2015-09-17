from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic

from braces.views import LoginRequiredMixin

from core.views import NeverCacheMixin, AccessControlMixin, ActionReloadView
from core.models import ProjectTracking, Project, User
from core.forms import CreateProjectForm


class ProjectAccessControlMixin(AccessControlMixin):
    """
    Implements AccessControlMixin for Project as kwarg to view.
    """

    def get_group_required(self):
        self.project = Project.objects.get(slug=self.kwargs.get('slug'))
        return super(ProjectAccessControlMixin, self).get_group_required(
            self.membership, self.project)


class ProjectListView(LoginRequiredMixin, NeverCacheMixin, generic.TemplateView):

    template_name = 'project_management/project_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        projects_tracked = [x.project_id for x in ProjectTracking.objects.filter(
            user=self.request.user) if x.project.is_viewer(self.request.user)]
        context['my_active_projects'] = Project.active_objects.filter(id__in=projects_tracked)
        context['active_projects'] = Project.active_objects.exclude(id__in=projects_tracked)
        context['inactive_projects'] = Project.inactive_objects.all()
        return context


class ProjectUpdateView(ProjectAccessControlMixin, generic.UpdateView):

    model = Project
    template_name = 'project_management/project_edit.html'
    form_class = CreateProjectForm

    membership = 'owner'

    def get_success_url(self):
        return reverse('pm_project_detail', args=(self.object.slug,))


class ProjectDetailView(ProjectAccessControlMixin, generic.DetailView):

    template_name = 'project_management/project_detail.html'
    model = Project

    membership = 'viewer'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['investigation_list'] = sorted(self.project.investigation_set.all(),
                                               key=lambda x: x.is_active, reverse=True)
        return context


class AddUserToProjectGroupView(ProjectAccessControlMixin, ActionReloadView):

    membership = 'owner'

    def perform_action(self, request, *args, **kwargs):
        self.project = Project.objects.get(slug=kwargs.pop('slug'))
        user = User.objects.get(username=kwargs.pop('username'))
        attribute = kwargs.pop('attribute')
        self.project.add_user(user, attribute)

    def get_redirect_url(self, **kwargs):
        return reverse('pm_project_detail', kwargs={'slug': self.project.slug})


class RemoveUserFromProjectGroup(ProjectAccessControlMixin, ActionReloadView):

    membership = 'owner'

    def perform_action(self, request, *args, **kwargs):
        self.project = Project.objects.get(slug=kwargs.pop('slug'))
        user = User.objects.get(username=kwargs.pop('username'))
        self.project.remove_user(user)

    def get_redirect_url(self, **kwargs):
        return reverse('pm_project_detail', kwargs={'slug': self.project.slug})
