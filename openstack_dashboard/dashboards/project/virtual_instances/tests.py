from django.urls import reverse_lazy
from horizon.test import helpers as horizon_helpers

from openstack_dashboard.dashboards.project.instances import tables
from openstack_dashboard.dashboards.project.virtual_instances import (
    tables as virtual_tables,
)
from openstack_dashboard.test import helpers

INDEX_URL = reverse_lazy("horizon:project:virtual_instances:index")


@horizon_helpers.pytest_mark("hybrid_site")
class VirtualLaunchWizardTests(helpers.TestCase):
    def _ngclick(self, action_class):
        action = action_class()
        action.table = virtual_tables.VirtualInstancesTable(self.request)
        action.get_default_attrs()
        return action.attrs["ng-click"]

    def test_virtual_launch_link_declares_virtual(self):
        ngclick = self._ngclick(tables.LaunchVirtualInstanceLinkNG)

        self.assertIn("instanceType: 'virtual'", ngclick)
        self.assertIn("successUrl: '%s'" % INDEX_URL, ngclick)
