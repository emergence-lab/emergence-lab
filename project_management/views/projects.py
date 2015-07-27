from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic

from braces.views import LoginRequiredMixin

from core.views import NeverCacheMixin
from core.models import ProjectTracking, Project


class ProjectListView(LoginRequiredMixin, NeverCacheMixin, generic.TemplateView):

    template_name = 'project_management/project_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        projects_tracked = [x.project_id for x in ProjectTracking.objects.filter(
            user=self.request.user)]
        context['my_active_projects'] = Project.active_objects.filter(id__in=projects_tracked)
        context['active_projects'] = Project.active_objects.exclude(id__in=projects_tracked)
        context['inactive_projects'] = Project.inactive_objects.all()
        return context


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):

    model = Project
    template_name = 'project_management/project_edit.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('pm_project_list')
