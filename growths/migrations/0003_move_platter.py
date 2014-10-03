# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_platter_data(apps, schema_editor):
    old_platter = apps.get_model('core', 'platter')
    new_platter = apps.get_model('growths', 'Platter')
    for platter in old_platter.objects.all():
        new_platter.objects.create(
            id=platter.id,
            name=platter.name,
            serial=platter.serial,
            start_date=platter.start_date,
            is_active=platter.is_active,
            status_changed=platter.status_changed
        )


def reverse_migrate_platter_data(apps, schema_editor):
    old_platter = apps.get_model('core', 'platter')
    new_platter = apps.get_model('growths', 'Platter')
    for platter in new_platter.objects.all():
        old_platter.objects.create(
            id=platter.id,
            name=platter.name,
            serial=platter.serial,
            start_date=platter.start_date,
            is_active=platter.is_active,
            status_changed=platter.status_changed
        )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_status_changed_not_editable'),
        ('growths', '0002_delete_serial_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Platter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('status_changed', models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True)),
                ('name', models.CharField(max_length=45, verbose_name='name')),
                ('serial', models.CharField(max_length=20, verbose_name='serial number', blank=True)),
                ('start_date', models.DateField(auto_now_add=True, verbose_name='date started')),
            ],
            options={
                'verbose_name': 'platter',
                'verbose_name_plural': 'platters',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='growth',
            name='platter',
            field=models.ForeignKey(to='growths.Platter'),
        ),
        migrations.RunPython(migrate_platter_data, reverse_migrate_platter_data),
    ]
