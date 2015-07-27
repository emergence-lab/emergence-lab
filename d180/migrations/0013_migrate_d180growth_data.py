# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations



def migrate_d180growth_forward(apps, schema_editor):
    """
    Assume D180GrowthInfo objects don't exist yet so create and copy data.
    """
    D180Process = apps.get_model('d180', 'D180Growth')
    D180GrowthInfo = apps.get_model('d180', 'D180GrowthInfo')

    for process in D180Process.objects.all():
        data = {
            'process': process,
            'platter': process.platter,
            'has_gan': process.has_gan,
            'has_aln': process.has_aln,
            'has_inn': process.has_inn,
            'has_algan': process.has_algan,
            'has_ingan': process.has_ingan,
            'other_material': process.other_material,
            'orientation': process.orientation,
            'is_template': process.is_template,
            'is_buffer': process.is_buffer,
            'has_pulsed': process.has_pulsed,
            'has_superlattice': process.has_superlattice,
            'has_mqw': process.has_mqw,
            'has_graded': process.has_graded,
            'has_n': process.has_n,
            'has_p': process.has_p,
            'has_u': process.has_u,
        }
        info = D180GrowthInfo.objects.create(**data)


def migrate_d180growth_backward(apps, schema_editor):
    """
    Assume both D180Growth and D180GrowthInfo objects exist, so copy data.
    """
    D180Process = apps.get_model('d180', 'D180Growth')
    D180GrowthInfo = apps.get_model('d180', 'D180GrowthInfo')

    for info in D180GrowthInfo.objects.all():
        process = info.process
        process.platter = info.platter
        process.has_gan = info.has_gan
        process.has_aln = info.has_aln
        process.has_inn = info.has_inn
        process.has_algan = info.has_algan
        process.has_ingan = info.has_ingan
        process.other_material = info.other_material
        process.orientation = info.orientation
        process.is_template = info.is_template
        process.is_buffer = info.is_buffer
        process.has_pulsed = info.has_pulsed
        process.has_superlattice = info.has_superlattice
        process.has_mqw = info.has_mqw
        process.has_graded = info.has_graded
        process.has_n = info.has_n
        process.has_p = info.has_p
        process.has_u = info.has_u
        process.save()



class Migration(migrations.Migration):

    dependencies = [
        ('d180', '0012_remove_investigations'),
    ]

    operations = [
        migrations.RunPython(migrate_d180growth_forward, migrate_d180growth_backward),
    ]
