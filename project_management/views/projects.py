from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic

from braces.views import LoginRequiredMixin

from core.views import NeverCacheMixin, AccessControlMixin
from core.models import ProjectTracking, Project


class ProjectAccessControlMixin(AccessControlMixin):
    """
    Implements AccessControlMixin for Project as kwarg to view.
    """

    membership = None

    def get_group_required(self):
        self.project = Project.objects.get(slug=self.kwargs.get('slug'))
        instance = self.project
        return super(ProjectAccessControlMixin, self).get_group_required(
            self.membership, instance)


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
    fields = '__all__'

    membership = 'owner'

    def get_success_url(self):
        return reverse('pm_project_list')
