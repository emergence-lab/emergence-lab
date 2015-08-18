from braces.views import GroupRequiredMixin


# class OwnerRequiredMixin(GroupRequiredMixin):
#
#     def get_group_required(self, instance):
#         return 'rbac_{0}_owner_{1}'.format(instance.__class__.__name__.lower(), instance.slug)
#
#
# class MemberRequiredMixin(GroupRequiredMixin):
#
#     def get_group_required(self, instance):
#         # object_type = None
#         # slug = None
#         return ['rbac_{0}_owner_{1}'.format(instance.__class__.__name__.lower(), instance.slug),
#             'rbac_{0}_member_{1}'.format(instance.__class__.__name__.lower(), instance.slug)]
#
#
# class ViewerRequiredMixin(GroupRequiredMixin):
#
#     def get_group_required(self, instance):
#         # object_type = None
#         # slug = None
#         return ['rbac_{0}_owner_{1}'.format(instance.__class__.__name__.lower(), instance.slug),
#             'rbac_{0}_member_{1}'.format(instance.__class__.__name__.lower(), instance.slug),
#             'rbac_{0}_viewer_{1}'.format(instance.__class__.__name__.lower(), instance.slug)]

class AccessControlMixin(GroupRequiredMixin):
    """
    A generic Role-Based Access Control Mixin to re-implement GroupRequiredMixin
    based on the access control groups defined in the models.
    """

    def get_group_required(self, membership, instance):
        if not membership in ['owner', 'member', 'viewer',]:
            raise Exception('RBAC: membership must be either owner, member, or viewer')
        groups = ['rbac_{0}_{1}_{2}'.format(instance.__class__.__name__.lower(),
                    'owner', instance.slug),]
        if membership in ['member', 'viewer']:
            groups += ['rbac_{0}_{1}_{2}'.format(instance.__class__.__name__.lower(),
                        'member', instance.slug),]
        if membership in ['owner', 'member', 'viewer']:
            groups += ['rbac_{0}_{1}_{2}'.format(instance.__class__.__name__.lower(),
                        'viewer', instance.slug),]
        return groups
