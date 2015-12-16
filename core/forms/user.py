# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.forms import UserCreationForm

from core.models import User


class CreateUserForm(UserCreationForm):
    """
    For administratively creating users.
    """
    class Meta:
        model = User
        fields = ('username', 'full_name', 'short_name', 'email',
                  'is_active', 'is_staff', 'is_superuser',)


class EditUserForm(UserCreationForm):
    """
    For a user to edit their attributes including password.
    """
    class Meta:
        model = User
        fields = ('username', 'full_name', 'short_name', 'email',)
