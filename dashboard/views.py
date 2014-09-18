from django.shortcuts import render
from django.views.generic import DetailView

from core.models import operator, project, investigation
from core.streams import operator_project_stream, operator_investigation_stream
from growths.models import growth
from journal.models import journal_entry


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
        try:
            self.object = operator.objects.get(user=request.user)
        except:
            self.object = operator(name=request.user.first_name, active=1, user=request.user)
            self.object.save()
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
        context['entries'] = (journal_entry.objects.filter(investigations__in=self.object.investigation_set.all(),
                                                           author_id=userid)
                                                    .order_by('-date')[:25])
        context['stream'] = operator_project_stream(self.request.user.operator, self.object)
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
        context['entries'] = (journal_entry.objects.filter(investigations__pk=self.object.id,
                                                           author_id=userid)
                                                    .order_by('-date')[:25])
        context['project'] = self.object.project
        context['stream'] = operator_investigation_stream(self.request.user.operator, self.object)
        return context
