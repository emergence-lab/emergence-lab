# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0004_d180growth_growth_number'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('status_changed', models.DateTimeField(verbose_name='status changed', null=True, editable=False, blank=True)),
                ('tool', models.CharField(max_length=10, choices=[(b'd180', b'D180'), (b'd75', b'D75')])),
                ('reservation_date', models.DateTimeField(auto_now_add=True)),
                ('growth_length_in_hours', models.DecimalField(max_digits=2, decimal_places=1)),
                ('comment', models.CharField(max_length=500, blank=True)),
                ('bake_length_in_minutes', models.IntegerField()),
                ('priority_field', models.BigIntegerField(default=9223372036854775807)),
                ('platter', models.ForeignKey(to='d180.Platter')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
