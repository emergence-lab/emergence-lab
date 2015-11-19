# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations



def create_default_process_category(apps, schema_editor):
    ProcessCategory = apps.get_model('core', 'ProcessCategory')

    ProcessCategory.objects.get_or_create(
        slug='uncategorized',
        name='Uncategorized',
        description='Uncategorized process types.')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151003_1009'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessCategory',
            fields=[
                ('slug', models.SlugField(default='uncategorized', max_length=100, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='processtype',
            name='category',
            field=models.ForeignKey(related_query_name='processtype', related_name='processtypes', default='uncategorized', to='core.ProcessCategory'),
        ),
        migrations.RunPython(create_default_process_category),
    ]
