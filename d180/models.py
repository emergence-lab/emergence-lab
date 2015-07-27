# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from collections import OrderedDict

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from core.models import ActiveStateMixin, Process


@python_2_unicode_compatible
class Platter(ActiveStateMixin, models.Model):
    """
    Stores platter information.
    """
    name = models.CharField(_('name'), max_length=45)
    serial = models.CharField(_('serial number'), max_length=20, blank=True)
    start_date = models.DateField(_('date started'), auto_now_add=True)

    class Meta:
        verbose_name = _('platter')
        verbose_name_plural = _('platters')

    def __str__(self):
        return self.name


class D180GrowthInfo(models.Model):
    """
    Stores information related to a growth on the d180 including tagging for
    material and device properties.
    """
    process = models.OneToOneField(Process, related_name='info')
    platter = models.ForeignKey(Platter,
                                limit_choices_to={'is_active': True})

    # layer materials
    has_gan = models.BooleanField(default=False)
    has_aln = models.BooleanField(default=False)
    has_inn = models.BooleanField(default=False)
    has_algan = models.BooleanField(default=False)
    has_ingan = models.BooleanField(default=False)
    other_material = models.CharField(max_length=50, blank=True)

    # layer orientation
    orientation = models.CharField(max_length=10, default='0001')

    # growth features
    is_template = models.BooleanField(default=False)
    is_buffer = models.BooleanField(default=False)
    has_pulsed = models.BooleanField(default=False)
    has_superlattice = models.BooleanField(default=False)
    has_mqw = models.BooleanField(default=False)
    has_graded = models.BooleanField(default=False)

    # doping features
    has_n = models.BooleanField(default=False)
    has_p = models.BooleanField(default=False)
    has_u = models.BooleanField(default=False)

    @property
    def material(self):
        print('material')
        materials = OrderedDict([
            (self.has_gan, 'GaN'),
            (self.has_aln, 'AlN'),
            (self.has_inn, 'InN'),
            (self.has_algan, 'AlGaN'),
            (self.has_ingan, 'InGaN'),
            (self.other_material, self.other_material),
        ])
        return ', '.join([v for k, v in materials.items() if k])

    @property
    def doping(self):
        dopings = OrderedDict([
            (self.has_n, 'n-type'),
            (self.has_p, 'p-type'),
            (self.has_u, 'unintentional'),
        ])
        return ', '.join(v for k, v in dopings.items() if k)

    @property
    def growth_features(self):
        features = OrderedDict([
            (self.is_template, 'is a template'),
            (self.is_buffer, 'is a buffer'),
            (self.has_pulsed, 'has pulsed layer(s)'),
            (self.has_superlattice, 'has superlattice layers'),
            (self.has_mqw, 'has multi-quantum well layers'),
            (self.has_graded, 'has graded composition layer(s)'),
        ])
        return ', '.join(v for k, v in features.items() if k)


@python_2_unicode_compatible
class D180Readings(models.Model):
    """
    Stores readings (i.e. temperature) from a d180 growth.
    """
    # growth and layer info
    process = models.ForeignKey(Process, related_name='readings')
    layer = models.IntegerField()
    description = models.CharField(max_length=100, blank=True)

    # readings
    pyro_out = models.DecimalField(max_digits=7, decimal_places=2)
    pyro_in = models.DecimalField(max_digits=7, decimal_places=2)
    ecp_temp = models.DecimalField(max_digits=7, decimal_places=2)
    tc_out = models.DecimalField(max_digits=7, decimal_places=2)
    tc_in = models.DecimalField(max_digits=7, decimal_places=2)
    motor_rpm = models.DecimalField(max_digits=7, decimal_places=2)
    gc_pressure = models.DecimalField(max_digits=7, decimal_places=2)
    gc_position = models.DecimalField(max_digits=7, decimal_places=2)
    voltage_in = models.DecimalField(max_digits=7, decimal_places=2)
    voltage_out = models.DecimalField(max_digits=7, decimal_places=2)
    current_in = models.DecimalField(max_digits=7, decimal_places=2)
    current_out = models.DecimalField(max_digits=7, decimal_places=2)
    top_vp_flow = models.DecimalField(max_digits=7, decimal_places=2)
    hydride_inner = models.DecimalField(max_digits=7, decimal_places=2)
    hydride_outer = models.DecimalField(max_digits=7, decimal_places=2)
    alkyl_flow_inner = models.DecimalField(max_digits=7, decimal_places=2)
    alkyl_push_inner = models.DecimalField(max_digits=7, decimal_places=2)
    alkyl_flow_middle = models.DecimalField(max_digits=7, decimal_places=2)
    alkyl_push_middle = models.DecimalField(max_digits=7, decimal_places=2)
    alkyl_flow_outer = models.DecimalField(max_digits=7, decimal_places=2)
    alkyl_push_outer = models.DecimalField(max_digits=7, decimal_places=2)
    n2_flow = models.DecimalField(max_digits=7, decimal_places=2)
    h2_flow = models.DecimalField(max_digits=7, decimal_places=2)
    nh3_flow = models.DecimalField(max_digits=7, decimal_places=2)
    hydride_pressure = models.DecimalField(max_digits=7, decimal_places=2)
    tmga1_flow = models.DecimalField(max_digits=7, decimal_places=2)
    tmga1_pressure = models.DecimalField(max_digits=7, decimal_places=2)
    tmga2_flow = models.DecimalField(max_digits=7, decimal_places=2)
    tmga2_pressure = models.DecimalField(max_digits=7, decimal_places=2)
    tega2_flow = models.DecimalField(max_digits=7, decimal_places=2)
    tega2_pressure = models.DecimalField(max_digits=7, decimal_places=2)
    tmin1_flow = models.DecimalField(max_digits=7, decimal_places=2)
    tmin1_pressure = models.DecimalField(max_digits=7, decimal_places=2)
    tmal1_flow = models.DecimalField(max_digits=7, decimal_places=2)
    tmal1_pressure = models.DecimalField(max_digits=7, decimal_places=2)
    cp2mg_flow = models.DecimalField(max_digits=7, decimal_places=2)
    cp2mg_pressure = models.DecimalField(max_digits=7, decimal_places=2)
    cp2mg_dilution = models.DecimalField(max_digits=7, decimal_places=2)
    silane_flow = models.DecimalField(max_digits=7, decimal_places=2)
    silane_dilution = models.DecimalField(max_digits=7, decimal_places=2)
    silane_mix = models.DecimalField(max_digits=7, decimal_places=2)
    silane_pressure = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = _('reading')
        verbose_name_plural = _('readings')

    def __str__(self):
        return self.process.__str__()


@python_2_unicode_compatible
class D180RecipeLayer(models.Model):
    """
    Stores layers used in the recipes for a d180 growth.
    """
    process = models.ForeignKey(Process, related_name='recipe')

    layer_num = models.IntegerField()
    loop_num = models.IntegerField()
    loop_repeats = models.IntegerField()
    time = models.IntegerField()

    cp2mg_flow = models.IntegerField()
    tmin1_flow = models.IntegerField()
    tmin2_flow = models.IntegerField()
    tmga1_flow = models.IntegerField()
    tmga2_flow = models.IntegerField()
    tmal1_flow = models.IntegerField()
    tega1_flow = models.IntegerField()
    cp2mg_press = models.IntegerField()
    tmin_press = models.IntegerField()
    tmin2_press = models.IntegerField()
    tmga1_press = models.IntegerField()
    tmga2_press = models.IntegerField()
    tmal1_press = models.IntegerField()
    tega1_press = models.IntegerField()
    cp2mg_push = models.IntegerField()
    hyd_outer = models.IntegerField()
    hyd_inner = models.IntegerField()
    top_vp = models.IntegerField()
    ring_purge = models.IntegerField()
    alk_inj_press = models.IntegerField()
    alk_diff_press = models.IntegerField()
    alk_inj_push = models.IntegerField()
    alk_vent_push = models.IntegerField()
    motor_rpm = models.IntegerField()
    sub_temp_outer = models.IntegerField()
    sub_temp_inner = models.IntegerField()
    n2_flow = models.IntegerField()
    gc_press = models.IntegerField()
    h2_flow = models.IntegerField()
    nh3_flow = models.IntegerField()
    sih4_flow = models.IntegerField()
    spare_1 = models.IntegerField()
    sih4_push = models.IntegerField()
    sih4_dd = models.IntegerField()
    sih4_press = models.IntegerField()
    gc_purge = models.IntegerField()
    alk_outer = models.IntegerField()
    alk_middle = models.IntegerField()
    alk_inner = models.IntegerField()
    hyd_line_press = models.IntegerField()
    tmin1_mol_frac = models.IntegerField()
    tmin2_mol_frac = models.IntegerField()
    nh3_cond = models.IntegerField()
    h2n2_switch = models.IntegerField()
    alk_push_inner = models.IntegerField()
    alk_push_middle = models.IntegerField()
    alk_push_outer = models.IntegerField()

    class Meta:
        verbose_name = _('layer')
        verbose_name_plural = _('layers')

    def __str__(self):
        return self.process.__str__()


@python_2_unicode_compatible
class D180Source(models.Model):
    """
    Stores information on source consumption
    """
    created = models.DateTimeField(auto_now_add=True)
    cp2mg = models.DecimalField(max_digits=7, decimal_places=2)
    tmin1 = models.DecimalField(max_digits=7, decimal_places=2)
    tmin2 = models.DecimalField(max_digits=7, decimal_places=2)
    tmga1 = models.DecimalField(max_digits=7, decimal_places=2)
    tmga2 = models.DecimalField(max_digits=7, decimal_places=2)
    tmal1 = models.DecimalField(max_digits=7, decimal_places=2)
    tega1 = models.DecimalField(max_digits=7, decimal_places=2)
    nh3 = models.DecimalField(max_digits=9, decimal_places=2)
    sih4 = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = _('source entry')
        verbose_name_plural = _('source entries')

    def __str__(self):
        return self.created
