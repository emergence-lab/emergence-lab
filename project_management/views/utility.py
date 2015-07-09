from __future__ import absolute_import, unicode_literals

from django.views import generic

from braces.views import LoginRequiredMixin
from actstream.models import model_stream

from core.models import ProjectTracking, Investigation, Process, Milestone
from project_management.models import Literature


class LandingPageView(LoginRequiredMixin, generic.TemplateView):

    template_name = 'project_management/landing_page.html'

    def get_context_data(self, **kwargs):
        context = super(LandingPageView, self).get_context_data(**kwargs)
        projects = [x.project for x in ProjectTracking.objects.all().filter(user=self.request.user)]
        context['projects'] = projects
        context['investigations'] = Investigation.objects.all().filter(project__in=projects)
        context['milestones'] = Milestone.objects.all().filter(
            user=self.request.user).filter(is_active=True)
        context['literature'] = Literature.objects.all().filter(user=self.request.user)
        return context


class NewsfeedView(LoginRequiredMixin, generic.TemplateView):

    template_name = 'project_management/newsfeed.html'

    def get_context_data(self, **kwargs):
        context = super(NewsfeedView, self).get_context_data(**kwargs)
        context['process_stream'] = model_stream(Process)[:20]
        return context