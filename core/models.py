from __future__ import unicode_literals

from django.db import models


#########################
# Simple Storage Models #
#########################

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


#################
# Growth Models #
#################

class growth(models.Model):
    REACTOR_CHOICES = [
        ('d180', 'D180'),
        ('d75', 'D75'),
    ]

    # general info
    growth_number = models.SlugField(max_length=10)
    date = models.DateField()
    operator = models.ForeignKey(operator, limit_choices_to={'active': True})
    project = models.ForeignKey(project, limit_choices_to={'active': True})
    investigation = models.ForeignKey(investigation, limit_choices_to={'active': True})
    platter = models.ForeignKey(platter, limit_choices_to={'active': True})
    reactor = models.CharField(max_length=10, choices=REACTOR_CHOICES)
    run_comments = models.TextField(blank=True)

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
    has_superlattice = models.BooleanField(default=False)
    has_mqw = models.BooleanField(default=False)
    has_graded = models.BooleanField(default=False)

    # doping features
    has_n = models.BooleanField(default=False)
    has_p = models.BooleanField(default=False)
    has_u = models.BooleanField(default=False)

    def __unicode__(self):
        return self.growth_number

    class Meta:
        db_table = 'growths'


class sample(models.Model):
    SUBSTRATE_CHOICES = [
        ('growth', 'Growth'),
        ('sapphire', 'Sapphire'),
        ('si', 'Silicon'),
        ('sic', 'Silicon Carbide'),
        ('bulk', 'Bulk III-N'),
    ]
    SIZE_CHOICES = [
        ('whole', 'Whole'),
        ('half', 'Half'),
        ('quarter', 'Quarter'),
        ('square_cm', 'Square cm'),
        ('other', 'Other'),
    ]

    growth = models.ForeignKey(growth)
    growth_number = models.CharField(max_length=10)
    pocket = models.IntegerField(default=1)
    piece = models.CharField(max_length=5, blank=True)  # i.e. abcd...
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='whole')
    location = models.CharField(max_length=50)
    substrate_type = models.CharField(max_length=20, choices=SUBSTRATE_CHOICES, default='sapphire')
    substrate_serial = models.CharField(max_length=20, blank=True)  # wafer serial or growth number
    substrate_orientation = models.CharField(max_length=10, default='0001')
    substrate_miscut = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    substrate_comment = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return '{0}_{1}{2}'.format(self.growth_number, self.pocket, self.piece)

    class Meta:
        db_table = 'samples'


###########################
# Characterization Models #
###########################

class afm(models.Model):
    LOCATION_CHOICES = [
        ('c', 'Center'),
        ('r', 'Round'),
        ('f', 'Flat'),
    ]

    growth = models.ForeignKey(growth)
    sample = models.ForeignKey(sample)
    growth_number = models.CharField(max_length=10)
    scan_number = models.IntegerField(default=0)

    rms = models.DecimalField(max_digits=7, decimal_places=3)
    zrange = models.DecimalField(max_digits=7, decimal_places=3)
    location = models.CharField(max_length=45, choices=LOCATION_CHOICES, default='c')
    size = models.DecimalField(max_digits=7, decimal_places=3)

    filename = models.CharField(max_length=150, blank=True)
    amplitude_filename = models.CharField(max_length=150, blank=True)

    def __unicode__(self):
        return '{0}_{1}.{2}'.format(self.growth_number, self.location,
                                    str(self.scan_number).zfill(3))

    class Meta:
        db_table = 'afm'
