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
from django.test import SimpleTestCase
from django.urls import reverse

import horizon


def declared_panel_group_slugs():
    return [config['PANEL_GROUP']
            for config in settings.HORIZON_CONFIG['panel_customization']
            if config.get('PANEL_GROUP') and not config.get('PANEL')]


def registered_panel_slugs(group_slug):
    # Dashboards and panels register while the URLconf is being built, from
    # Site._urls(). Resolve a URL first or the registry is empty here.
    reverse('horizon:project:instances:index')
    groups = horizon.get_dashboard('project').get_panel_groups()
    return [panel.slug for panel in groups[group_slug]]


class ComputePanelGroupTests(SimpleTestCase):
    """Chameleon Feature: baremetal and virtual compute are separate groups.

    A file in openstack_dashboard/enabled/ that raises is skipped with only a
    log warning, so a broken panel group fails nothing on its own.
    """

    def test_both_groups_are_declared(self):
        slugs = declared_panel_group_slugs()

        self.assertIn('compute', slugs)
        self.assertIn('virtual_compute', slugs)

    def test_virtual_group_is_empty_on_a_baremetal_only_site(self):
        """The reason the group can be declared unconditionally.

        CHAMELEON_ENABLE_VMS is False under the test settings, so
        VirtualInstances.can_register() denies registration and the slug is
        never appended to the group -- horizon/base.py:968 returns before the
        append at :974. _sidebar.html wraps the group heading in
        `{% if filtered_panels %}`, so an empty group renders nothing at all.
        """
        self.assertEqual([], registered_panel_slugs('virtual_compute'))

    def test_baremetal_group_keeps_the_upstream_panels(self):
        """The rename is display-only; the slug and its panels do not move."""
        slugs = registered_panel_slugs('compute')

        for expected in ('overview', 'instances', 'images', 'key_pairs'):
            self.assertIn(expected, slugs)
