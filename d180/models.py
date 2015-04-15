# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from core.models import ActiveStateMixin, Process, Investigation


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


@python_2_unicode_compatible
class D180Growth(Process):
    """
    Stores information related to a growth on the d180 including tagging for
    material and device properties.
    """
    name = 'D180 Growth'
    slug = 'd180-growth'
    is_destructive = True

    # general info
    investigations = models.ManyToManyField(Investigation,
        related_name='growths', related_query_name='growth',)
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

    class Meta:
        verbose_name = _('d180 growth')
        verbose_name_plural = _('d180 growths')

    def __str__(self):
        return self.uuid


@python_2_unicode_compatible
class D180Readings(models.Model):
    """
    Stores readings (i.e. temperature) from a d180 growth.
    """
    # growth and layer info
    growth = models.ForeignKey(D180Growth, related_name='readings')
    layer = models.IntegerField()
    layer_desc = models.CharField(max_length=45, blank=True)

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
        return self.growth.__str__()


@python_2_unicode_compatible
class D180RecipeLayer(models.Model):
    """
    Stores layers used in the recipes for a d180 growth.
    """
    growth = models.ForeignKey(D180Growth)

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
        return self.growth.__str__()


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
