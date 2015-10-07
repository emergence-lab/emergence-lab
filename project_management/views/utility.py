from __future__ import absolute_import, unicode_literals

from django.views import generic

from braces.views import LoginRequiredMixin
from actstream.models import model_stream

from core.models import Process, Task
from project_management.models import Literature


class LandingPageView(LoginRequiredMixin, generic.TemplateView):

    template_name = 'project_management/landing_page.html'

    def get_context_data(self, **kwargs):
        context = super(LandingPageView, self).get_context_data(**kwargs)
        user = self.request.user
        context['projects'] = user.get_projects('viewer', followed=True)
        context['investigations'] = user.get_investigations('viewer', followed=True)
        context['milestones'] = user.get_milestones('viewer', followed=True)
        context['literature'] = Literature.objects.all().filter(user=self.request.user)
        context['tasks'] = Task.objects.all().filter(
            user=self.request.user).filter(is_active=True)
        return context


class NewsfeedView(LoginRequiredMixin, generic.TemplateView):

    template_name = 'project_management/newsfeed.html'

    def get_context_data(self, **kwargs):
        context = super(NewsfeedView, self).get_context_data(**kwargs)
        stream = model_stream(Process)
        context['process_stream'] = stream[:20]
        context['my_process_stream'] = [x for x in stream if x.actor == self.request.user][:20]
        return context
