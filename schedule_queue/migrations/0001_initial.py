# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('d180', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('status_changed', models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('reservation_date', models.DateTimeField(auto_now_add=True)),
                ('growth_length', models.DecimalField(max_digits=2, decimal_places=1)),
                ('comment', models.CharField(max_length=500, blank=True)),
                ('bake_length', models.IntegerField()),
                ('priority', models.BigIntegerField(default=9223372036854775807)),
                ('platter', models.ForeignKey(to='d180.Platter')),
                ('tool', models.ForeignKey(related_query_name='reservation', related_name='reservations', to='core.ProcessType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
