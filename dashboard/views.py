from django.views.generic import DetailView

from braces.views import LoginRequiredMixin

from core.models import operator, Project, Investigation
from core.streams import project_stream, investigation_stream
from growths.models import growth
from schedule_queue.models import Reservation, tools


class DashboardMixin(object):
    """
    Mixin that populates the context with active and inactive projects.
    """
    def get_context_data(self, **kwargs):
        projects = operator.objects.filter(user=self.request.user).values_list('projects__id', flat=True)
        kwargs['active_projects'] = Project.active_objects.filter(id__in=projects)
        kwargs['inactive_projects'] = Project.inactive_objects.filter(id__in=projects)
        return super(DashboardMixin, self).get_context_data(**kwargs)


class Dashboard(LoginRequiredMixin, DashboardMixin, DetailView):
    """
    Main dashboard for the user with commonly used actions.
    """
    template_name = 'dashboard/dashboard.html'
    model = operator
    object = None

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['growths'] = growth.objects.filter(operator=self.object).order_by('-growth_number')[:25]
        reservation_list = []
        for i in tools.get_tool_list():
            reservation_list.append(Reservation.objects.filter(is_active=True, tool=i).order_by('priority_field').first())
        context['reservations'] = reservation_list
        context['tools'] = tools.get_tool_list()
        return context

    def get_object(self, queryset=None):
        return self.object

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = operator.objects.get(user=request.user)
        except:
            self.object = operator(name=request.user.first_name, user=request.user)
            self.object.save()
        return super(Dashboard, self).dispatch(request, *args, **kwargs)


class ProjectDetailDashboardView(LoginRequiredMixin, DashboardMixin, DetailView):
    """
    View for details of a project in the dashboard.
    """
    template_name = 'dashboard/project_detail_dashboard.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailDashboardView, self).get_context_data(**kwargs)
        context['growths'] = (growth.objects.filter(project=self.object)
                                            .order_by('-growth_number')[:25])
        context['stream'] = project_stream(self.object)
        return context


class InvestigationDetailDashboardView(LoginRequiredMixin, DashboardMixin, DetailView):
    """
    View for details of an investigation in the dashboard.
    """
    template_name = 'dashboard/investigation_detail_dashboard.html'
    model = Investigation

    def get_context_data(self, **kwargs):
        context = super(InvestigationDetailDashboardView, self).get_context_data(**kwargs)
        context['growths'] = (growth.objects.filter(investigation=self.object)
                                            .order_by('-growth_number')[:25])
        context['project'] = self.object.project
        context['stream'] = investigation_stream(self.object)
        return context
