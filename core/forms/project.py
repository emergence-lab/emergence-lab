# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from core.models import Investigation, Project, ProjectTracking


class TrackProjectForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.active_objects.all())

    def save(self, **kwargs):
        commit = kwargs.pop('commit', True)
        user = kwargs.pop('user', None)

        instance = super(TrackProjectForm, self).save(commit=False)
        instance.user = user

        if commit:
            instance.save()

        return instance

    class Meta:
        model = ProjectTracking
        fields = ('project', 'is_owner',)


class CreateProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description',)
        widgets = {
            'description': forms.Textarea(attrs={'class': 'hallo'}),
            'owner_group': forms.HiddenInput(),
            'member_group': forms.HiddenInput(),
            'viewer_group': forms.HiddenInput(),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        reserved_names = [
            'create',
            'track',
            'all',
            'list',
        ]
        if name in reserved_names:
            self.add_error('name',
                'Project name "{}" is reserved, please choose another'.format(name))
        return name


class CreateInvestigationForm(forms.ModelForm):

    class Meta:
        model = Investigation
        fields = ('name', 'description',)

    def clean_name(self):
        name = self.cleaned_data['name']
        reserved_names = [
            'activate',
            'deactivate',
            'add-investigation',
            'all',
            'list',
        ]
        if name in reserved_names:
            self.add_error('name',
                'Investigation name "{}" is reserved, please choose another'.format(name))
        return name
