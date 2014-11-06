from django.db import models

from core.models import TimestampMixin


class BaseProcess(TimestampMixin, models.Model):
    """
    Base class for all processes.
    """
    comment = models.TextField(blank=True)

    class Meta:
        abstract = True
