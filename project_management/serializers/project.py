from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from core.models import Project, Investigation, Milestone


class AccessControlModelSerializer(serializers.ModelSerializer):

    owner_group = serializers.StringRelatedField()
    member_group = serializers.StringRelatedField()
    viewer_group = serializers.StringRelatedField()


class MilestoneSerializer(AccessControlModelSerializer):

    class Meta:
        model = Milestone
        fields = ('name', 'slug', 'owner_group', 'member_group',
                  'viewer_group', 'description',)


class InvestigationSerializer(AccessControlModelSerializer):

    milestones = MilestoneSerializer(many=True, read_only=True)

    class Meta:
        model = Investigation
        fields = ('name', 'slug', 'description', 'owner_group', 'member_group',
                  'viewer_group', 'milestones',)


class ProjectSerializer(AccessControlModelSerializer):

    investigations = InvestigationSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('name', 'slug', 'description', 'owner_group', 'member_group',
                  'viewer_group', 'investigations',)
