# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from inspect import isclass

from django.core.exceptions import ImproperlyConfigured
from django.db import models

import actstream.registry
import six

from .mixins import TimestampMixin


class BaseProcess(TimestampMixin, models.Model):
    """
    Base class for all processes.
    """
    comment = models.TextField(blank=True)
    destructive = models.BooleanField(default=True)

    class Meta:
        abstract = True


def validate(model_class, exception_class=ImproperlyConfigured):
    if isinstance(model_class, six.string_types):
        model_class = models.get_model(*model_class.split('.'))
    if not issubclass(model_class, BaseProcess):
        raise exception_class(
            'Object {0} is not a process model. Process models should inherit '
            'from BaseProcess'.format(model_class))
    if model_class._meta.abstract:
        raise exception_class(
            'Model {0} is abstract, so it cannot be registered as a '
            'process'.format(model_class))
    if not actstream.registry.is_installed(model_class):
        raise exception_class(
            'The model {0} is not installed, please put the app {1} in your '
            'INSTALLED_APPS setting'.format(model_class,
                                            model_class._meta.app_label))
    return model_class


class ProcessRegistry(dict):

    def register(self, *model_classes_or_labels):
        for class_or_label in model_classes_or_labels:
            model_class = validate(class_or_label)
            if model_class not in self:
                self[model_class] = model_class
                actstream.registry.register(model_class)

    def unregister(self, *model_classes_or_labels):
        for class_or_label in model_classes_or_labels:
            model_class = validate(class_or_label)
            if model_class in self:
                del self[model_class]
                actstream.registry.unregister(model_class)

    def check(self, model_class_or_object):
        if not isclass(model_class_or_object):
            model_class_or_object = model_class_or_object.__class__
        model_class = validate(model_class_or_object, RuntimeError)
        if model_class not in self:
            raise ImproperlyConfigured(
                'The model {0} is not registered. Use process.registry to '
                'register it.'.format(model_class.__name__))
        actstream.registry.check(model_class_or_object)

    def get_process_choices(self):
        limit = None
        for process_class in six.iterkeys(self):
            app_label = m._meta.app_label
            model = m.__name__
            if limit is None:
                limit = models.Q(app_label=app_label, model=model)
            else:
                limit = limit | models.Q(app_label=app_label, model=model)
        return limit


registry = ProcessRegistry()
register = registry.register
unregister = registry.unregister
get_process_choices = registry.get_process_choices
check = registry.check
