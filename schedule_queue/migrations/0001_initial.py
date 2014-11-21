# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('growths', '0007_auto_20141120_2233'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tool', models.CharField(max_length=10)),
                ('reservation_date', models.DateTimeField(auto_now_add=True)),
                ('growth_length_in_hours', models.DecimalField(max_digits=2, decimal_places=1)),
                ('comment', models.CharField(max_length=500, blank=True)),
                ('bake_length_in_minutes', models.IntegerField()),
                ('priority_field', models.IntegerField(default=2147483647)),
                ('is_active', models.BooleanField(default=True)),
                ('platter', models.ForeignKey(to='growths.Platter')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
