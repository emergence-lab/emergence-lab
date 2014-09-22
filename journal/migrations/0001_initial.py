# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'journal_entry'
        db.create_table(u'journal_entries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('entry', self.gf('markupfield.fields.MarkupField')(rendered_field=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('entry_markup_type', self.gf('django.db.models.fields.CharField')(default=u'markdown', max_length=30, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.operator'])),
            ('_entry_rendered', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(u'author',), max_length=50, populate_from=u'title')),
        ))
        db.send_create_signal(u'journal', ['journal_entry'])

        # Adding M2M table for field investigations on 'journal_entry'
        m2m_table_name = db.shorten_name(u'journal_entries_investigations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('journal_entry', models.ForeignKey(orm[u'journal.journal_entry'], null=False)),
            ('investigation', models.ForeignKey(orm[u'core.investigation'], null=False))
        ))
        db.create_unique(m2m_table_name, ['journal_entry_id', 'investigation_id'])


    def backwards(self, orm):
        # Deleting model 'journal_entry'
        db.delete_table(u'journal_entries')

        # Removing M2M table for field investigations on 'journal_entry'
        db.delete_table(db.shorten_name(u'journal_entries_investigations'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.investigation': {
            'Meta': {'object_name': 'investigation', 'db_table': "u'investigations'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('ckeditor.fields.RichTextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.project']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "u'name'"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.operator': {
            'Meta': {'object_name': 'operator', 'db_table': "u'operators'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.project']", 'through': u"orm['core.project_tracking']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'core.project': {
            'Meta': {'object_name': 'project', 'db_table': "u'projects'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'core': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('ckeditor.fields.RichTextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "u'name'"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.project_tracking': {
            'Meta': {'object_name': 'project_tracking', 'db_table': "u'project_operator_tracking'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_pi': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.operator']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.project']"})
        },
        u'journal.journal_entry': {
            'Meta': {'object_name': 'journal_entry', 'db_table': "u'journal_entries'"},
            '_entry_rendered': ('django.db.models.fields.TextField', [], {}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.operator']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entry': ('markupfield.fields.MarkupField', [], {'rendered_field': 'True', 'blank': 'True'}),
            'entry_markup_type': ('django.db.models.fields.CharField', [], {'default': "u'markdown'", 'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investigations': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.investigation']", 'symmetrical': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': "(u'author',)", 'max_length': '50', 'populate_from': "u'title'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['journal']