# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf import settings
from django.utils.translation import gettext_lazy as _

import horizon


class Instances(horizon.Panel):
    name = _("Instances")
    slug = 'instances'
    permissions = ('openstack.services.compute',)


class VirtualInstances(Instances):
    """CHI: the instances panel again, under the "Virtual Machines" group.

    Reuses every view, table and action from Instances; only the index view
    and the URL namespace differ. A distinct slug is required rather than
    stylistic: Dashboard.get_panel_groups() does registered.pop(
    panel.__class__), so registering one class under two groups raises
    KeyError and 500s the sidebar on every page.
    """

    name = _("Instances")
    slug = 'instances_virtual'
    urls = 'openstack_dashboard.dashboards.project.instances.vm_urls'

    @staticmethod
    def can_register():
        return settings.CHAMELEON_ENABLE_VMS
