from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic

from braces.views import LoginRequiredMixin

from core.models import ProjectTracking, Investigation
from project_management.models import Milestone, Literature


class LandingPageView(LoginRequiredMixin, generic.TemplateView):

    template_name = 'project_management/landing_page.html'

    def get_context_data(self, **kwargs):
        context = super(LandingPageView, self).get_context_data(**kwargs)
        projects = [x.project for x in ProjectTracking.objects.all().filter(user=self.request.user)]
        context['projects'] = projects
        context['investigations'] = Investigation.objects.all().filter(project__in=projects)
        context['milestones'] = Milestone.objects.all().filter(user=self.request.user).filter(is_active=True)
        context['literature'] = Literature.objects.all().filter(user=self.request.user)
        return context
