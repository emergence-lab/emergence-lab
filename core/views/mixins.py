from braces.views import GroupRequiredMixin


class AccessControlMixin(GroupRequiredMixin):
    """
    A generic Role-Based Access Control Mixin to re-implement GroupRequiredMixin
    based on the access control groups defined in the models.
    """

    membership = None

    def get_group_required(self, membership, instance):
        if membership not in ['owner', 'member', 'viewer']:
            raise Exception('RBAC: membership must be either owner, member, or viewer')
        groups = [instance.owner_group.name]
        if membership in ['member', 'viewer']:
            groups += [instance.member_group.name]
        if membership in ['owner', 'member', 'viewer']:
            groups += [instance.member_group, instance.viewer_group.name]
        return groups
