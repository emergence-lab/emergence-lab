import re

from django.db import models
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from ckeditor.fields import RichTextField

import core.models


class growth(models.Model):
    """
    Stores information related to the growth including tagging for material
    and device properties.
    """
    REACTOR_CHOICES = [
        ('d180', 'D180'),
        ('d75', 'D75'),
    ]

    # general info
    growth_number = models.SlugField(max_length=10)
    date = models.DateField()
    operator = models.ForeignKey(core.models.operator,
                                 limit_choices_to={'is_active': True})
    project = models.ForeignKey(core.models.project,
                                limit_choices_to={'is_active': True})
    investigation = models.ForeignKey(core.models.investigation,
                                      limit_choices_to={'is_active': True})
    platter = models.ForeignKey(core.models.platter,
                                limit_choices_to={'is_active': True})
    reactor = models.CharField(max_length=10, choices=REACTOR_CHOICES)
    run_comments = RichTextField(blank=True)

    # layer materials
    has_gan = models.BooleanField(default=False)
    has_aln = models.BooleanField(default=False)
    has_inn = models.BooleanField(default=False)
    has_algan = models.BooleanField(default=False)
    has_ingan = models.BooleanField(default=False)
    has_alingan = models.BooleanField(default=False)
    other_material = models.CharField(max_length=50, blank=True)

    # layer orientation
    orientation = models.CharField(max_length=10, default='0001')

    # growth features
    is_template = models.BooleanField(default=False)
    is_buffer = models.BooleanField(default=False)
    has_superlattice = models.BooleanField(default=False)
    has_mqw = models.BooleanField(default=False)
    has_graded = models.BooleanField(default=False)

    # doping features
    has_n = models.BooleanField(default=False)
    has_p = models.BooleanField(default=False)
    has_u = models.BooleanField(default=False)

    def __unicode__(self):
        return self.growth_number

    @staticmethod
    def get_growth(growth_number):
        """
        Returns the growth associated with the growth number or raises the
        specified exception on errors
        """
        m = re.match('([gt][1-9][0-9]{3,})(?:\_([1-6])([a-z]*))?', growth_number)
        if not m:
            raise Exception('Growth {0} improperly formatted'.format(growth_number))

        try:
            obj = growth.objects.get(growth_number=growth_number)
        except MultipleObjectsReturned:
            raise Exception('Growth {0} ambiguous'.format(growth_number))
        except ObjectDoesNotExist:
            raise Exception('Growth {0} does not exist'.format(growth_number))
        return obj

    class Meta:
        db_table = 'growths'


class sample(models.Model):
    """
    Stores information for an individual sample from a growth. Used as a
    reference for characteriztion data.
    """
    SUBSTRATE_CHOICES = [
        ('growth', 'Growth'),
        ('sapphire', 'Sapphire'),
        ('si', 'Silicon'),
        ('sic', 'Silicon Carbide'),
        ('bulk', 'Bulk III-N'),
        ('other', 'Other'),
    ]
    SIZE_CHOICES = [
        ('whole', 'Whole'),
        ('half', 'Half'),
        ('quarter', 'Quarter'),
        ('square_cm', 'Square cm'),
        ('other', 'Other'),
    ]

    growth = models.ForeignKey(growth)
    pocket = models.CharField(max_length=10, default='1')
    parent = models.ForeignKey('self', blank=True, null=True)
    piece = models.CharField(max_length=5, blank=True)  # i.e. abcd...
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='whole')
    location = models.CharField(max_length=50)  # i.e. lab, w/ collaborator, etc.
    substrate_type = models.CharField(max_length=20, choices=SUBSTRATE_CHOICES, default='sapphire')
    substrate_serial = models.CharField(max_length=20, blank=True)  # wafer serial or growth number
    substrate_orientation = models.CharField(max_length=10, default='0001')
    substrate_miscut = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    comment = RichTextField(blank=True)

    def __unicode__(self):
        return '{0}_{1}{2}'.format(self.growth.growth_number, self.pocket, self.piece)

    @staticmethod
    def get_sample(sample_name, growth_object=None):
        """
        Returns the sample associated with the name or raises the
        specified exception on errors.

        growth_object may optionally be specified with a growth instance to
        prevent duplicate queries.
        """
        # extract information from sample name
        m = re.match('([gt][1-9][0-9]{3,})(?:\_([0-9]+\-?[0-9]*)([a-z]*))?', sample_name)
        if not m:
            raise Exception('Sample {0} improperly formatted'.format(sample_name))

        # query for the growth if it wasn't specified
        if growth_object is None:
            growth_object = growth.get_growth(m.group(1))
        elif growth_object.growth_number != m.group(1):
            raise Exception('Sample {0} does not match the growth {1}'.format(sample_name, growth_object.growth_number))
        filter_params = {'growth': growth_object}

        # check if pocket or piece are specified
        if m.group(2):
            filter_params['pocket'] = int(m.group(2))
        if m.group(3):
            filter_params['piece'] = m.group(3)

        try:
            obj = sample.objects.get(**filter_params)
        except MultipleObjectsReturned:
            raise Exception('Sample {0} ambiguous'.format(sample_name))
        except ObjectDoesNotExist:
            raise Exception('Sample {0} does not exist'.format(sample_name))
        return obj

    @staticmethod
    def get_siblings(sample_obj):
        """
        Return a queryset of samples that are siblings of the specified sample.

        A sibling is defined as a sample that was in the same growth.
        """
        return sample.objects.filter(growth=sample_obj.growth).exclude(pk=sample_obj.id)

    @staticmethod
    def get_children(sample_obj):
        """
        Return a queryset of samples that are children of the specified sample.

        A child is defined as a sample that has the current sample marked as a parent.
        """
        return sample_obj.sample_set.exclude(pk=sample_obj.pk)

    @staticmethod
    def get_piece_siblings(sample_obj):
        """
        Return a queryset of samples that are piece siblings of the specified sample.

        A piece sibling is defined as samples that were split from the same piece.
        """
        return sample.objects.filter(growth=sample_obj.growth, pocket=sample_obj.pocket).exclude(pk=sample_obj.id)

    def split(self, number_pieces):
        """
        Splits a sample into the specified number of pieces. Sets the size to 'other'.
        Parent is inherited from the original sample.
        """
        siblings = sample.objects.filter(growth=self.growth, pocket=self.pocket).order_by('-piece')
        parent = self
        original_id = self.id
        original_parent_id = self.parent_id
        self.save()
        new_pieces = [parent]
        if len(siblings) > 1:
            last_letter = siblings.first().piece
        else:
            last_letter = 'a'
            parent.piece = 'a'
            parent.size = 'other'
            parent.save()
        for i in range(number_pieces - 1):
            if last_letter != 'z':
                last_letter = unichr(ord(last_letter) + 1)
            else:
                raise Exception('Too many pieces')
            print(last_letter)
            parent.pk = None
            parent.parent = None
            parent.piece = last_letter
            parent.size = 'other'
            parent.save()
            if original_parent_id == original_id:
                parent.parent = parent
            else:
                parent.parent_id = original_parent_id
            parent.save()
            new_pieces.append(parent)
        return new_pieces

    class Meta:
        db_table = 'samples'


class readings(models.Model):
    """
    Stores readings (i.e. temperature) from a growth.
    """
    # growth and layer info
    growth = models.ForeignKey(growth)
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

    def __unicode__(self):
        return self.growth.growth_number

    class Meta:
        db_table = 'readings'


class recipe_layer(models.Model):
    """
    Stores layers used in the recipes
    """
    growth = models.ForeignKey(growth)
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

    def __unicode__(self):
        return self.growth.growth_number

    class Meta:
        db_table = 'recipe_layers'


class source(models.Model):
    """
    Stores information on source consumption
    """
    cp2mg = models.DecimalField(max_digits=7, decimal_places=2)
    tmin1 = models.DecimalField(max_digits=7, decimal_places=2)
    tmin2 = models.DecimalField(max_digits=7, decimal_places=2)
    tmga1 = models.DecimalField(max_digits=7, decimal_places=2)
    tmga2 = models.DecimalField(max_digits=7, decimal_places=2)
    tmal1 = models.DecimalField(max_digits=7, decimal_places=2)
    tega1 = models.DecimalField(max_digits=7, decimal_places=2)
    nh3 = models.DecimalField(max_digits=9, decimal_places=2)
    sih4 = models.DecimalField(max_digits=9, decimal_places=2)
    date_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.date_time

    class Meta:
        db_table = 'sources'
