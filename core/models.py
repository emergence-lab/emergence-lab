# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class operator(models.Model):
    name = models.CharField(max_length=45)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'operators'


class platter(models.Model):
    name = models.CharField(max_length=45)
    active = models.BooleanField(default=True)
    serial = models.CharField(max_length=20, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'platters'


class project(models.Model):
    name = models.CharField(max_length=45)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'projects'


class investigation(models.Model):
    name = models.CharField(max_length=45)
    active = models.BooleanField(default=True)
    projects = models.ManyToManyField(project)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'investigations'


class growth(models.Model):
    id = models.IntegerField(primary_key=True)
    growth_number = models.SlugField(max_length=10)
    date = models.DateField(blank=True, null=True)
    operator = models.CharField(max_length=45, blank=True)
    project = models.CharField(max_length=45, blank=True)
    investigation = models.CharField(max_length=100, blank=True)
    reactor_select = models.CharField(max_length=45, blank=True)
    run_comments = models.CharField(max_length=1000, blank=True)
    carrier_number = models.CharField(max_length=45, blank=True)

    # pocket
    p1_sub_number = models.CharField(max_length=45, blank=True)
    p1_run_number = models.CharField(max_length=45, blank=True)
    p1_polish = models.CharField(max_length=45, blank=True)
    p2_sub_number = models.CharField(max_length=45, blank=True)
    p2_run_number = models.CharField(max_length=45, blank=True)
    p2_polish = models.CharField(max_length=45, blank=True)
    p3_sub_number = models.CharField(max_length=45, blank=True)
    p3_run_number = models.CharField(max_length=45, blank=True)
    p3_polish = models.CharField(max_length=45, blank=True)
    p4_sub_number = models.CharField(max_length=45, blank=True)
    p4_run_number = models.CharField(max_length=45, blank=True)
    p4_polish = models.CharField(max_length=45, blank=True)
    p5_sub_number = models.CharField(max_length=45, blank=True)
    p5_run_number = models.CharField(max_length=45, blank=True)
    p5_polish = models.CharField(max_length=45, blank=True)
    p6_sub_number = models.CharField(max_length=45, blank=True)
    p6_run_number = models.CharField(max_length=45, blank=True)
    p6_polish = models.CharField(max_length=45, blank=True)

    # growth tags
    layerhas_gan = models.IntegerField(blank=True, null=True)
    layerhas_algan = models.IntegerField(blank=True, null=True)
    layerhas_ingan = models.IntegerField(blank=True, null=True)
    layerhas_aln = models.IntegerField(blank=True, null=True)
    layerhas_other = models.CharField(max_length=45, blank=True)
    layeris_ntype = models.IntegerField(blank=True, null=True)
    layeris_ptype = models.IntegerField(blank=True, null=True)
    layeris_uid = models.IntegerField(blank=True, null=True)
    substrate_orient_c = models.IntegerField(blank=True, null=True)
    substrate_orient_a = models.IntegerField(blank=True, null=True)
    substrate_orient_m = models.IntegerField(blank=True, null=True)
    substrateis_orient_r = models.IntegerField(blank=True, null=True)
    substrate_orient_other = models.IntegerField(blank=True, null=True)
    is_template = models.IntegerField(blank=True, null=True)
    substrate_is = models.CharField(max_length=45, blank=True)
    layerhas_superlattice = models.IntegerField(blank=True, null=True)
    layerhas_mqw = models.IntegerField(blank=True, null=True)
    layerhas_sqw = models.IntegerField(blank=True, null=True)
    film_orient_c = models.IntegerField(blank=True, null=True)
    film_orient_a = models.IntegerField(blank=True, null=True)
    film_orient_m = models.IntegerField(blank=True, null=True)
    film_orient_r = models.IntegerField(blank=True, null=True)
    film_orient_other = models.IntegerField(blank=True, null=True)

    # checklist / run logging
    chk_pre_rcp = models.IntegerField(blank=True, null=True)
    chk_pre_openll = models.IntegerField(db_column='chk_pre_openLL', blank=True, null=True)  # Field name made lowercase.
    chk_pre_load = models.IntegerField(blank=True, null=True)
    chk_pre_closell = models.IntegerField(db_column='chk_pre_closeLL', blank=True, null=True)  # Field name made lowercase.
    chk_pre_alk = models.IntegerField(blank=True, null=True)
    chk_pre_hyd = models.IntegerField(blank=True, null=True)
    chk_pre_llpres = models.DecimalField(db_column='chk_pre_LLpres', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    chk_pre_opengv = models.IntegerField(db_column='chk_pre_openGV', blank=True, null=True)  # Field name made lowercase.
    chk_pre_trans = models.IntegerField(blank=True, null=True)
    chk_pre_rot = models.IntegerField(blank=True, null=True)
    chk_pre_closegv = models.IntegerField(db_column='chk_pre_closeGV', blank=True, null=True)  # Field name made lowercase.
    chk_pre_final = models.IntegerField(blank=True, null=True)
    chk_pre_epi = models.IntegerField(blank=True, null=True)
    chk_start = models.IntegerField(blank=True, null=True)
    chk_post_idle = models.IntegerField(blank=True, null=True)
    chk_post_episave = models.IntegerField(blank=True, null=True)
    chk_post_opengv = models.IntegerField(db_column='chk_post_openGV', blank=True, null=True)  # Field name made lowercase.
    chk_post_trans = models.IntegerField(blank=True, null=True)
    chk_post_closegv = models.IntegerField(db_column='chk_post_closeGV', blank=True, null=True)  # Field name made lowercase.
    chk_post_llpres = models.DecimalField(db_column='chk_post_LLpres', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    chk_post_openll = models.IntegerField(db_column='chk_post_openLL', blank=True, null=True)  # Field name made lowercase.
    chk_post_closell = models.IntegerField(db_column='chk_post_closeLL', blank=True, null=True)  # Field name made lowercase.
    chk_post_alk = models.IntegerField(blank=True, null=True)

    cl_1 = models.IntegerField(blank=True, null=True)
    cl_2 = models.IntegerField(blank=True, null=True)
    cl_3 = models.IntegerField(blank=True, null=True)
    cl_4 = models.IntegerField(blank=True, null=True)
    cl_5 = models.IntegerField(blank=True, null=True)
    cl_1_laynum = models.CharField(max_length=45, blank=True)
    cl_2_laynum = models.CharField(max_length=45, blank=True)
    cl_3_laynum = models.CharField(max_length=45, blank=True)
    cl_4_laynum = models.CharField(max_length=45, blank=True)
    cl_5_laynum = models.CharField(max_length=45, blank=True)
    cl_1_lay_purp = models.CharField(max_length=45, blank=True)
    cl_2_lay_purp = models.CharField(max_length=45, blank=True)
    cl_3_lay_purp = models.CharField(max_length=45, blank=True)
    cl_4_lay_purp = models.CharField(max_length=45, blank=True)
    cl_5_lay_purp = models.CharField(max_length=45, blank=True)
    pyro_out_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    pyro_in_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    fil_in_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    fil_out_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    motor_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gc_pres_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gc_pos_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    volt_in_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    curr_in_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    vol_out_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    curr_out_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    vp_flow_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_in_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_out_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_in_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_push_in_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_mid_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_push_mid_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_out_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_push_out_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    n2_flow_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    h2_flow_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    nh3_flow_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_pres_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga1_flow_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga1_pres_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga2_flow_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga2_pres_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tega1_flow_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tega1_pres_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmin1_flow_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmin1_pres_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmal1_flow_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmal1_pres_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    cp2mg1_flow_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    cp2_mg1_pres_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sih4_flow_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sih4_pres_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gr_rate_cl_1 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    pyro_out_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    pyro_in_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    fil_in_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    fil_out_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    motor_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gc_pres_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gc_pos_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    volt_in_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    curr_in_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    volt_out_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    curr_out_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    vp_flow_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_in_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_out_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_in_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_pres_in_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_mid_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_pres_mid_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_out_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_pres_out_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    n2_flow_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    h2_flow_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    nh3_flow_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_pres_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga1_flow_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga1_pres_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga2_flow_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga2_pres_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tega1_flow_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tega1_pres_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmin1_flow_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmin1_pres_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmal1_flow_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmal1_pres_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    cp2mg1_flow_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    cp2mg1_pres_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sih4_flow_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sih4_pres_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gr_rate_cl_2 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    pyro_out_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    pyro_in_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    fil_in_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    fil_out_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    motor_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gc_pres_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gc_pos_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    volt_in_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    curr_in_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    volt_out_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    curr_out_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    vp_flow_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_in_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_out_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_in_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_pres_in_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_mid_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_pres_mid_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_out_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_pres_out_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    n2_flow_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    h2_flow_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    nh3_flow_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_pres_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga1_flow_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga1_pres_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga2_flow_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga2_pres_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tega1_flow_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tega1_pres_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmin1_flow_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmin1_pres_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmal1_flow_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmal1_pres_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    cp2mg1_flow_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    cp2mg1_pres_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sih4_flow_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sih4_pres_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gr_rate_cl_3 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    pyro_out_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    pyro_in_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    fil_in_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    fil_out_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    motor_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gc_pres_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gc_pos_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    volt_in_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    curr_in_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    volt_out_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    curr_out_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    vp_flow_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_in_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_out_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_in_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_pres_in_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_mid_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_pres_mid_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_out_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_pres_out_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    n2_flow_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    h2_flow_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    nh3_flow_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_pres_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga1_flow_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga1_pres_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga2_flow_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga2_pres_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tega1_flow_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tega1_pres_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmin1_flow_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmin1_pres_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmal1_flow_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmal1_pres_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    cp2mg1_flow_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    cp2mg1_pres_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sih4_flow_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sih4_pres_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gr_rate_cl_4 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    pyro_out_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    pyro_in_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    fil_in_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    fil_out_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    motor_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gc_pres_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gc_pos_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    volt_in_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    curr_in_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    volt_out_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    curr_out_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    vp_flow_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_in_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_out_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_in_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_pres_in_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_mid_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_pres_mid_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_flow_out_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    alk_pres_out_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    n2_flow_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    h2_flow_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    nh3_flow_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    hyd_pres_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga1_flow_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga1_pres_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga2_flow_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga2_pres_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tega1_flow_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tega1_pres_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmin1_flow_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmin1_pres_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmal1_flow_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmal1_pres_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    cp2mg1_flow_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    cp2mg1_pres_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sih4_flow_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sih4_pres_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    gr_rate_cl_5 = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    cp2mg1_pre_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmin1_pre_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga1_pre_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga2_pre_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmal1_pre_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tega1_pre_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    nh3_pre_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sih4_pre_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    cp2mg1_post_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmin1_post_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga1_post_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga2_post_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmal1_post_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tega1_post_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    nh3_post_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sih4_post_amt = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    cp2mg1_temp = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmin1_temp = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga1_temp = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmga2_temp = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tmal1_temp = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    tega1_temp = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    def __unicode__(self):
        return self.growth_number

    class Meta:
        db_table = 'growths'


class afm(models.Model):
    id = models.IntegerField(primary_key=True)
    growth = models.ForeignKey(growth)
    growth_number = models.CharField(max_length=20)
    pocket = models.IntegerField(default=1)
    scan_number = models.IntegerField(default=0)

    rms = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True)
    zrange = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True)
    location = models.CharField(max_length=45, blank=True)
    size = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True)

    filename = models.CharField(max_length=150, blank=True)
    amplitude_filename = models.CharField(max_length=150, blank=True)

    def __unicode__(self):
        return '{0}_{1}_{2}.{3}'.format(self.growth_number, self.pocket, self.location.lower()[0],
                                        str(self.scan_number).zfill(3))

    class Meta:
        db_table = 'afm'
