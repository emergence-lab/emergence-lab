# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .mixins import (
    AccessControlMixin,
)
from .utility import (
    AboutView,
    ActiveListView,
    ActionReloadView,
    ExceptionHandlerView,
    HomepageView,
    ProtectedMediaView,
    QuickSearchRedirectView,
    PrintTemplate,
    NeverCacheMixin,
)
from .user import (
    ActivateUserRedirectView,
    DeactivateUserRedirectView,
    UserListView,
)
from .project import (
    ActivateProjectRedirectView,
    DeactivateProjectRedirectView,
    ProjectCreateView,
    # ProjectDetailView,
    # ProjectListView,
    # ProjectUpdateView,
    TrackProjectRedirectView,
    TrackProjectView,
    UntrackProjectRedirectView,
    ActivateInvestigationRedirectView,
    DeactivateInvestigationRedirectView,
    # InvestigationCreateView,
    # InvestigationDetailView,
    # InvestigationListView,
    # InvestigationUpdateView,
)
from .sample import (
    SampleDetailView,
    SampleListView,
    SampleCreateView,
    SampleUpdateView,
    SampleSplitView,
    SampleSearchView,
    ExportSampleDetail,
)
from .process import (
    ProcessDetailView,
    ProcessListRedirectView,
    ProcessListView,
    ProcessUpdateView,
    RunProcessView,
    UploadFileView,
    ProcessTemplateListView,
    AddProcessTemplateView,
    ProcessTemplateDetailView,
    ProcessTemplateEditView,
    RemoveProcessTemplateView,
    ProcessWizardView,
    TemplateProcessWizardView,
    ProcessTypeListView,
    ProcessTypeDetailView,
    ProcessTypeUpdateView,
    ProcessTypeCreateView,
)
