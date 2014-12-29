# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .misc import (ActiveListView,
                   ExceptionHandlerView,
                   HomepageView,
                   protected_media,
                   QuickSearchRedirectView)
from .user import (ActivateUserRedirectView,
                   DeactivateUserRedirectView,
                   UserListView)
from .project import (ActivateProjectRedirectView,
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
                      InvestigationUpdateView)
