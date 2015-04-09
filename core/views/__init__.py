# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .utility import (
    AboutView,
    ActiveListView,
    ActionReloadView,
    ExceptionHandlerView,
    HomepageView,
    ProtectedMediaView,
    QuickSearchRedirectView,
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
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
    TrackProjectRedirectView,
    TrackProjectView,
    UntrackProjectRedirectView,
    ActivateInvestigationRedirectView,
    DeactivateInvestigationRedirectView,
    InvestigationCreateView,
    InvestigationDetailView,
    InvestigationListView,
    InvestigationUpdateView,
)
from .sample import (
    SampleDetailView,
    SampleListView,
    SampleCreateView,
    SampleUpdateView,
    SampleSearchView,
)
from .process import (
    ProcessDetailView,
    ProcessCreateView,
    ProcessListView,
    ProcessUpdateView,
    RunProcessView,
    CreateUploadProcessView,
    UploadFileView,
)
