from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic

from braces.views import LoginRequiredMixin

from core.models import User, Project


class ProjectListView(LoginRequiredMixin, generic.TemplateView):

    template_name = 'project_management/project_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        projects = (User.objects.filter(pk=self.request.user.id)
                                .values_list('projects__id', flat=True))
        context['active_projects'] = Project.active_objects.filter(id__in=projects)
        return context
