from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
import os
from django.utils import timezone
import storages.backends.s3boto
from django.utils.deconstruct import deconstructible
import datetime

import aws_support as aws

from core.models import Investigation


@deconstructible
class FixedS3BotoStorage(storages.backends.s3boto.S3BotoStorage):
    pass

protected_storage = FixedS3BotoStorage(acl='private',
                                       querystring_auth=True,
                                       querystring_expire=600,
                                       # 10 minutes, try to ensure people won't/can't share
                                       )


def content_file_name(instance, filename):
    return ''.join(('simulations/',
                    str(instance.user.username),
                    str("_"),
                    datetime.datetime.strftime(instance.request_date, '%Y_%m_%d_%H_%M_%S'),
                    str(os.path.splitext(filename)[1])))


@python_2_unicode_compatible
class Simulation(models.Model):

    def get_instance_types():
        """
        NOTE NOT REDUNDANT - Formats instance types for model choices.
        """
        m = aws.EC2Connection(settings.AWS_EC2_REGION,
                                 settings.AWS_ACCESS_KEY_ID,
                                 settings.AWS_SECRET_ACCESS_KEY)
        tmp = []
        for key in m.instance_detail_list().keys():
            desc = key.split('.')
            desc = str('{0} ({1})'.format(desc[1], desc[0]))
            tmp.append((key, desc))
        return tmp

    def is_completed(self):
        return self.finish_date is not None

    def elapsed_time(self):
        if self.start_date is None:
            return 0

        if self.finish_date is None:
            return timezone.now() - self.start_date

        return self.finish_date - self.start_date

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    investigations = models.ManyToManyField(Investigation)
    request_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)
    finish_date = models.DateTimeField(null=True, blank=True)
    file_path = models.FileField(
        null=True,
        blank=True,
        help_text='ZIP File with all simulation data',
        storage=protected_storage,
        upload_to=content_file_name
    )
    priority = models.BooleanField(default=False)
    execution_node = models.CharField(max_length=15, choices=get_instance_types())

    def __str__(self):              # __unicode__ on Python 2
        return '{0}, {1}, {2}, {3}'.format(str(self.user),
                                           str(self.is_completed()),
                                           str(self.request_date),
                                           str(self.id))
