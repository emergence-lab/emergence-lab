# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.apps.registry import Apps
from django.db import connection
from django.db.migrations.state import ProjectState
from django.test import TestCase

from core.migration_operations import PublishAppConfiguration
from core.models import AppConfigurationDefault

class TestAppConfigurationMigrationOperations(TestCase):

    def test_publish_empty_args(self):
        migration = PublishAppConfiguration(key=None)
        old_state = ProjectState(real_apps=['core'])
        # old_state.add_model('core', 'AppConfigurationDefault')
        new_state = old_state.clone()
        with connection.schema_editor() as editor:
            migration.database_forwards('test', editor, old_state, new_state)
        config = AppConfigurationDefault.objects.first()
        raise Exception(config)
