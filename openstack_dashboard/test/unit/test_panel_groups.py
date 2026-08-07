# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.conf import settings
from django.test import SimpleTestCase


def panel_group_slugs():
    return [config['PANEL_GROUP']
            for config in settings.HORIZON_CONFIG['panel_customization']
            if config.get('PANEL_GROUP') and not config.get('PANEL')]


def panels_in_group(slug):
    return [config['PANEL']
            for config in settings.HORIZON_CONFIG['panel_customization']
            if config.get('PANEL_GROUP') == slug and config.get('PANEL')]


class BaremetalComputePanelGroupTests(SimpleTestCase):
    """Chameleon Feature: the project compute panels are grouped as baremetal.

    A file in openstack_dashboard/enabled/ that raises is skipped with only a
    log warning, so a missing panel group does not fail anywhere on its own.
    """

    def test_panel_group_is_registered(self):
        self.assertIn('baremetal_compute', panel_group_slugs())

    def test_compute_panels_moved_into_it(self):
        self.assertEqual(['overview', 'instances', 'images', 'key_pairs'],
                         panels_in_group('baremetal_compute'))
