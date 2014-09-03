from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.contenttypes.models import ContentType

from actstream.models import actor_stream

from core.models import operator, project, investigation
from growths.models import growth


class DashboardMixin(object):

    def get_context_data(self, **kwargs):
        projects = operator.objects.filter(user=self.request.user).values_list('projects__id', flat=True)
        kwargs['active_projects'] = project.current.filter(id__in=projects)
        kwargs['inactive_projects'] = project.retired.filter(id__in=projects)
        return super(DashboardMixin, self).get_context_data(**kwargs)


class Dashboard(DashboardMixin, DetailView):
    """
    Main dashboard for the user with commonly used actions.
    """
    template_name = 'dashboard/dashboard.html'
    model = operator
    object = None

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['growths'] = growth.objects.filter(operator=self.object).order_by('-growth_number')[:25]
        return context

    def get_object(self, queryset=None):
        return self.object

    def dispatch(self, request, *args, **kwargs):
        self.object = operator.objects.get(user=request.user)
        return super(Dashboard, self).dispatch(request, *args, **kwargs)


class ProjectDetailDashboardView(DashboardMixin, DetailView):
    """
    View for details of a project in the dashboard.
    """
    template_name = 'dashboard/project_detail_dashboard.html'
    model = project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailDashboardView, self).get_context_data(**kwargs)
        userid = operator.objects.filter(user__username=self.request.user.username).values('id')
        context['growths'] = (growth.objects.filter(project=self.object,
                                                    operator_id=userid)
                                            .order_by('-growth_number')[:25])
        project_content_id = ContentType.objects.get(name='project').id
        context['stream'] = (actor_stream(self.request.user.operator).filter(target_content_type_id=project_content_id,
                                                                    target_object_id=self.object.id)
                            | actor_stream(self.request.user.operator).filter(action_object_content_type_id=project_content_id,
                                                                     action_object_object_id=self.object.id))
        return context


class InvestigationDetailDashboardView(DashboardMixin, DetailView):
    """
    View for details of an investigation in the dashboard.
    """
    template_name = 'dashboard/investigation_detail_dashboard.html'
    model = investigation

    def get_context_data(self, **kwargs):
        context = super(InvestigationDetailDashboardView, self).get_context_data(**kwargs)
        userid = operator.objects.filter(user__username=self.request.user.username).values('id')
        context['growths'] = (growth.objects.filter(project=self.object,
                                                    operator_id=userid)
                                            .order_by('-growth_number')[:25])
        context['project'] = self.object.project
        return context
