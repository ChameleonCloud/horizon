from django.conf import settings
from django.utils.translation import gettext_lazy as _

import horizon


class VirtualInstances(horizon.Panel):
    name = _("Instances")
    slug = 'virtual_instances'
    permissions = ('openstack.services.compute',)

    @staticmethod
    def can_register():
        return settings.CHAMELEON_ENABLE_VMS
