# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'operator'
        db.create_table(u'operators', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'core', ['operator'])

        # Adding model 'platter'
        db.create_table(u'platters', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('serial', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['platter'])

        # Adding model 'project'
        db.create_table(u'projects', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'core', ['project'])

        # Adding model 'investigation'
        db.create_table(u'investigations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'core', ['investigation'])

        # Adding M2M table for field projects on 'investigation'
        m2m_table_name = db.shorten_name(u'investigations_projects')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('investigation', models.ForeignKey(orm[u'core.investigation'], null=False)),
            ('project', models.ForeignKey(orm[u'core.project'], null=False))
        ))
        db.create_unique(m2m_table_name, ['investigation_id', 'project_id'])

        # Adding model 'growth'
        db.create_table(u'growths', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('growth_number', self.gf('django.db.models.fields.SlugField')(max_length=10)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('operator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.operator'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.project'])),
            ('investigation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.investigation'])),
            ('platter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.platter'])),
            ('reactor', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('run_comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('has_gan', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_aln', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_inn', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_algan', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_ingan', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_alingan', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('other_material', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('orientation', self.gf('django.db.models.fields.CharField')(default=u'0001', max_length=10)),
            ('is_template', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_superlattice', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_mqw', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_graded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_n', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_p', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_u', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'core', ['growth'])

        # Adding model 'sample'
        db.create_table(u'samples', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('growth', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.growth'])),
            ('growth_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('pocket', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('piece', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('size', self.gf('django.db.models.fields.CharField')(default=u'whole', max_length=20)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('substrate_type', self.gf('django.db.models.fields.CharField')(default=u'sapphire', max_length=20)),
            ('substrate_serial', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('substrate_orientation', self.gf('django.db.models.fields.CharField')(default=u'0001', max_length=10)),
            ('substrate_miscut', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=4, decimal_places=1)),
            ('substrate_comment', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'core', ['sample'])

        # Adding model 'afm'
        db.create_table(u'afm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('growth', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.growth'])),
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.sample'])),
            ('growth_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('scan_number', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rms', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=3)),
            ('zrange', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=3)),
            ('location', self.gf('django.db.models.fields.CharField')(default=u'c', max_length=45)),
            ('size', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=3)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('amplitude_filename', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
        ))
        db.send_create_signal(u'core', ['afm'])


    def backwards(self, orm):
        # Deleting model 'operator'
        db.delete_table(u'operators')

        # Deleting model 'platter'
        db.delete_table(u'platters')

        # Deleting model 'project'
        db.delete_table(u'projects')

        # Deleting model 'investigation'
        db.delete_table(u'investigations')

        # Removing M2M table for field projects on 'investigation'
        db.delete_table(db.shorten_name(u'investigations_projects'))

        # Deleting model 'growth'
        db.delete_table(u'growths')

        # Deleting model 'sample'
        db.delete_table(u'samples')

        # Deleting model 'afm'
        db.delete_table(u'afm')


    models = {
        u'core.afm': {
            'Meta': {'object_name': 'afm', 'db_table': "u'afm'"},
            'amplitude_filename': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'growth': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.growth']"}),
            'growth_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "u'c'", 'max_length': '45'}),
            'rms': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.sample']"}),
            'scan_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'size': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'}),
            'zrange': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'})
        },
        u'core.growth': {
            'Meta': {'object_name': 'growth', 'db_table': "u'growths'"},
            'date': ('django.db.models.fields.DateField', [], {}),
            'growth_number': ('django.db.models.fields.SlugField', [], {'max_length': '10'}),
            'has_algan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_alingan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_aln': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_gan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_graded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_ingan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_inn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_mqw': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_n': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_superlattice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_u': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investigation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.investigation']"}),
            'is_template': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.operator']"}),
            'orientation': ('django.db.models.fields.CharField', [], {'default': "u'0001'", 'max_length': '10'}),
            'other_material': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'platter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.platter']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.project']"}),
            'reactor': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'run_comments': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'core.investigation': {
            'Meta': {'object_name': 'investigation', 'db_table': "u'investigations'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.project']", 'symmetrical': 'False'})
        },
        u'core.operator': {
            'Meta': {'object_name': 'operator', 'db_table': "u'operators'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'core.platter': {
            'Meta': {'object_name': 'platter', 'db_table': "u'platters'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.project': {
            'Meta': {'object_name': 'project', 'db_table': "u'projects'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'core.sample': {
            'Meta': {'object_name': 'sample', 'db_table': "u'samples'"},
            'growth': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.growth']"}),
            'growth_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'piece': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'pocket': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'size': ('django.db.models.fields.CharField', [], {'default': "u'whole'", 'max_length': '20'}),
            'substrate_comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'substrate_miscut': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '1'}),
            'substrate_orientation': ('django.db.models.fields.CharField', [], {'default': "u'0001'", 'max_length': '10'}),
            'substrate_serial': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'substrate_type': ('django.db.models.fields.CharField', [], {'default': "u'sapphire'", 'max_length': '20'})
        }
    }

    complete_apps = ['core']