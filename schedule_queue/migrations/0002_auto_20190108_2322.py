# Generated by Django 2.1.5 on 2019-01-08 23:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_queue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='platter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='d180.Platter'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]