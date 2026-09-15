import html
import re

from django.test.utils import override_settings
from django import urls as django_urls
from horizon.test import helpers as horizon_helpers

from openstack_dashboard import api
from openstack_dashboard.dashboards.admin.instances import tables \
    as admin_tables
from openstack_dashboard.dashboards.project.instances import console
from openstack_dashboard.dashboards.project.instances import interfaces_tables
from openstack_dashboard.dashboards.project.instances import tables
from openstack_dashboard.test import helpers

VIRTUAL_PANEL = "/project/virtual_instances/"
DEFAULT_PANEL = "/project/instances/"
ADMIN_PANEL = "/admin/instances/"

INDEX_MOCKS = {
    api.nova: ("flavor_list", "server_list_paged",
               "tenant_absolute_limits", "is_feature_available"),
    api.glance: ("image_list_detailed",),
    api.neutron: ("floating_ip_simple_associate_supported",
                  "floating_ip_supported"),
    api.network: ("servers_update_addresses",),
    api.cinder: ("volume_list",),
}


@horizon_helpers.pytest_mark("hybrid_site")
class VirtualPanelRouteTests(helpers.TestCase):
    def test_a_default_panel_route_reverses_under_this_panel(self):
        self.assertEqual(
            VIRTUAL_PANEL + "i1/rebuild",
            django_urls.reverse(
                "horizon:project:virtual_instances:rebuild", args=["i1"]))

    def test_reverse_picks_this_panel_when_given_current_app(self):
        self.assertEqual(
            VIRTUAL_PANEL + "i1/rebuild",
            django_urls.reverse(
                "horizon:project:instances:rebuild", args=["i1"],
                current_app="horizon:project:virtual_instances"))

    def test_reverse_picks_the_default_panel_without_current_app(self):
        self.assertEqual(
            DEFAULT_PANEL + "i1/rebuild",
            django_urls.reverse(
                "horizon:project:instances:rebuild", args=["i1"]))


@horizon_helpers.pytest_mark("hybrid_site")
class VirtualPanelNavigationTests(helpers.TestCase):
    """A user acting on a VM must not land in the default compute panel."""

    def _get_index(self):
        self.mock_is_feature_available.return_value = True
        self.mock_flavor_list.return_value = self.flavors.list()
        self.mock_image_list_detailed.return_value = (
            self.images.list(), False, False)
        self.mock_server_list_paged.return_value = [
            self.servers.list(), False, False]
        self.mock_servers_update_addresses.return_value = None
        self.mock_tenant_absolute_limits.return_value = self.limits["absolute"]
        self.mock_floating_ip_supported.return_value = True
        self.mock_floating_ip_simple_associate_supported.return_value = True
        self.mock_volume_list.return_value = []
        page = self.client.get(VIRTUAL_PANEL)
        self.assertEqual(200, page.status_code)
        return page

    @helpers.create_mocks(INDEX_MOCKS)
    def test_the_launch_button_returns_the_user_to_this_panel(self):
        page = html.unescape(self._get_index().content.decode("utf-8"))

        self.assertIn("launch-virtual-ng", page)
        self.assertIn("instanceType: 'virtual'", page)
        self.assertIn("successUrl: '%s'" % VIRTUAL_PANEL, page)

    @override_settings(OPENSTACK_ENABLE_PASSWORD_RETRIEVE=True)
    @helpers.create_mocks(INDEX_MOCKS)
    def test_the_row_action_links_stay_out_of_the_default_panel(self):
        table = self._get_index().context["virtual_instances_table"]
        server = self.servers.first()

        strays = {action.name: action.bound_url
                  for action in table.get_row_actions(server)
                  if getattr(action, "bound_url", "").startswith(DEFAULT_PANEL)}

        self.assertEqual({}, strays)

    @helpers.create_mocks(INDEX_MOCKS)
    def test_the_instance_name_links_into_the_panel(self):
        table = self._get_index().context["virtual_instances_table"]
        tail = "%s/" % self.servers.first().id

        link = table.get_rows()[0].cells["name"].url

        self.assertEqual(VIRTUAL_PANEL + tail, link)

    def _interface_action_link(self, action, server, port):
        detail = VIRTUAL_PANEL + "%s/" % server.id
        request = self.factory.get(detail)
        request.resolver_match = django_urls.resolve(detail)
        action.table = interfaces_tables.InterfacesTable(
            request, [port], instance_id=server.id)
        return action.get_link_url(port)

    @helpers.create_mocks({api.neutron: ("is_extension_supported",)})
    def test_the_interface_edit_port_button_stays_in_the_panel(self):
        self.mock_is_extension_supported.return_value = True
        server = self.servers.first()
        port = [p for p in self.ports.list() if p.device_id == server.id][0]
        tail = "%s/ports/%s/update?step=update_info" % (server.id, port.id)

        link = self._interface_action_link(
            interfaces_tables.UpdatePort(), server, port)

        self.assertEqual(VIRTUAL_PANEL + tail, link)

    @helpers.create_mocks({api.neutron: ("is_extension_supported",)})
    def test_the_interface_security_groups_button_stays_in_the_panel(self):
        self.mock_is_extension_supported.return_value = True
        server = self.servers.first()
        port = [p for p in self.ports.list() if p.device_id == server.id][0]
        tail = ("%s/ports/%s/update?step=update_security_groups"
                % (server.id, port.id))

        link = self._interface_action_link(
            interfaces_tables.UpdateSecurityGroups(), server, port)

        self.assertEqual(VIRTUAL_PANEL + tail, link)

    def _assert_form_posts_to_the_panel(self, res, tail):
        self.assertEqual(200, res.status_code)
        found = re.search(r'<form [^>]*action="([^"]*)"',
                          res.content.decode("utf-8"))
        self.assertEqual(VIRTUAL_PANEL + tail,
                         found.group(1) if found else "rendered no form")

    @helpers.create_mocks({api.glance: ("image_list_detailed",)})
    def test_the_rescue_form_posts_to_the_panel(self):
        self.mock_image_list_detailed.return_value = (
            self.images.list(), False, False)
        tail = "%s/rescue" % self.servers.first().id

        self._assert_form_posts_to_the_panel(
            self.client.get(VIRTUAL_PANEL + tail), tail)

    @helpers.create_mocks({api.glance: ("image_list_detailed",),
                           api.nova: ("server_get", "is_feature_available")})
    def test_the_rebuild_form_posts_to_the_panel(self):
        server = self.servers.first()
        self.mock_image_list_detailed.return_value = (
            self.images.list(), False, False)
        self.mock_server_get.return_value = server
        self.mock_is_feature_available.return_value = False
        tail = "%s/rebuild" % server.id

        self._assert_form_posts_to_the_panel(
            self.client.get(VIRTUAL_PANEL + tail), tail)

    @helpers.create_mocks({api.neutron: ("network_list_for_tenant",
                                         "port_list_with_trunk_types")})
    def test_the_attach_interface_form_posts_to_the_panel(self):
        self.mock_network_list_for_tenant.return_value = self.networks.list()
        self.mock_port_list_with_trunk_types.return_value = self.ports.list()
        tail = "%s/attach_interface" % self.servers.first().id

        self._assert_form_posts_to_the_panel(
            self.client.get(VIRTUAL_PANEL + tail), tail)

    @helpers.create_mocks({api.neutron: ("network_list_for_tenant",
                                         "port_list_with_trunk_types")})
    def test_the_attach_interface_cancel_returns_to_the_panel(self):
        self.mock_network_list_for_tenant.return_value = self.networks.list()
        self.mock_port_list_with_trunk_types.return_value = self.ports.list()
        tail = "%s/attach_interface" % self.servers.first().id

        res = self.client.get(VIRTUAL_PANEL + tail)

        self.assertEqual(VIRTUAL_PANEL, res.context_data["cancel_url"])

    @helpers.create_mocks({api.neutron: (
        "floating_ip_target_list_by_instance", "tenant_floating_ip_list")})
    def test_the_disassociate_form_posts_to_the_panel(self):
        server = self.servers.first()
        port = [p for p in self.ports.list() if p.device_id == server.id][0]
        fip = self.floating_ips.first()
        fip.port_id = port.id
        self.mock_floating_ip_target_list_by_instance.return_value = [
            api.neutron.FloatingIpTarget(
                port, port["fixed_ips"][0]["ip_address"], server.name)]
        self.mock_tenant_floating_ip_list.return_value = [fip]
        tail = "%s/disassociate" % server.id

        self._assert_form_posts_to_the_panel(
            self.client.get(VIRTUAL_PANEL + tail), tail)

    @helpers.create_mocks({api.nova: ("server_get", "server_resize",
                                      "flavor_list", "flavor_get",
                                      "is_feature_available")})
    def test_the_resize_workflow_returns_to_the_panel(self):
        server = self.servers.first()
        new_flavor = [f for f in self.flavors.list()
                      if f.id != server.flavor["id"]][0]
        self.mock_server_get.return_value = server
        self.mock_flavor_list.return_value = self.flavors.list()

        res = self.client.post(VIRTUAL_PANEL + "%s/resize" % server.id,
                               {"flavor": new_flavor.id})

        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, VIRTUAL_PANEL)

    @helpers.create_mocks({api.neutron: ("port_get", "port_update",
                                         "is_extension_supported",
                                         "security_group_list")})
    def test_the_port_update_workflow_returns_to_the_panel(self):
        server = self.servers.first()
        port = [p for p in self.ports.list() if p.device_id == server.id][0]
        self.mock_port_get.return_value = port
        self.mock_port_update.return_value = port
        self.mock_is_extension_supported.return_value = False
        self.mock_security_group_list.return_value = self.security_groups.list()

        res = self.client.post(
            VIRTUAL_PANEL + "%s/ports/%s/update" % (server.id, port.id),
            {"name": port.name, "admin_state": port.is_admin_state_up})

        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, VIRTUAL_PANEL + "%s/" % server.id)

    @override_settings(CONSOLE_TYPE="SERIAL")
    @helpers.create_mocks({api.nova: ("server_get", "flavor_get",
                                      "instance_volumes_list",
                                      "is_feature_available"),
                           api.network: ("servers_update_addresses",),
                           api.neutron: ("is_extension_supported",
                                         "server_security_groups"),
                           console: ("get_console",)})
    def test_the_serial_console_stays_in_the_panel(self):
        server = self.servers.first()
        self.mock_server_get.return_value = server
        self.mock_flavor_get.return_value = self.flavors.first()
        self.mock_servers_update_addresses.return_value = None
        self.mock_server_security_groups.return_value = []
        self.mock_is_feature_available.return_value = True
        self.mock_is_extension_supported.return_value = True
        self.mock_instance_volumes_list.return_value = []
        self.mock_get_console.return_value = ("SERIAL", "ws://host/?token=t")
        tail = "%s/?tab=instance_details__console" % server.id

        res = self.client.get(VIRTUAL_PANEL + tail,
                              HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(
            [VIRTUAL_PANEL + "%s/serial" % server.id],
            re.findall(r'<iframe id="console_embed" src="([^"]*)"',
                       res.content.decode("utf-8")))

    @helpers.create_mocks({api.nova: ("server_get", "server_rebuild",
                                      "is_feature_available"),
                           api.glance: ("image_list_detailed",)})
    def test_a_failed_rebuild_returns_the_user_to_the_panel(self):
        server = self.servers.first()
        self.mock_server_get.return_value = server
        self.mock_image_list_detailed.return_value = (
            self.images.list(), False, False)
        self.mock_is_feature_available.return_value = False
        self.mock_server_rebuild.side_effect = self.exceptions.nova

        res = self.client.post(VIRTUAL_PANEL + "%s/rebuild" % server.id,
                               {"instance_id": server.id,
                                "image": self.images.first().id})

        self.assertRedirectsNoFollow(res, VIRTUAL_PANEL)

    @helpers.create_mocks({api.nova: ("server_get",)})
    def test_a_missing_instance_returns_the_user_to_the_panel(self):
        self.mock_server_get.side_effect = self.exceptions.nova

        res = self.client.get(
            VIRTUAL_PANEL + "%s/" % self.servers.first().id)

        self.assertRedirectsNoFollow(res, VIRTUAL_PANEL)

    @helpers.create_mocks({api.nova: ("server_get",)})
    def test_a_failed_resize_page_returns_the_user_to_the_panel(self):
        self.mock_server_get.side_effect = self.exceptions.nova

        res = self.client.get(
            VIRTUAL_PANEL + "%s/resize" % self.servers.first().id)

        self.assertRedirectsNoFollow(res, VIRTUAL_PANEL)

    @helpers.create_mocks({api.nova: ("get_password",)})
    def test_the_retrieve_password_page_keeps_the_user_here(self):
        self.mock_get_password.return_value = "encrypted"
        server = self.servers.first()
        tail = "%s/%s/decryptpassword" % (server.id, server.key_name)

        res = self.client.get(VIRTUAL_PANEL + tail)

        self._assert_form_posts_to_the_panel(res, tail)
        # base.html carries a modal skeleton whose cancel has no href.
        cancels_to = [href for href in re.findall(
            r'<a href="([^"]*)" class="btn btn-default cancel"',
            res.content.decode("utf-8")) if href.startswith("/")]
        self.assertEqual([VIRTUAL_PANEL], cancels_to)


@horizon_helpers.pytest_mark("hybrid_site")
class ReusedActionTests(helpers.TestCase):
    """Panels beyond these two reuse the same LinkAction classes."""

    def test_the_admin_rebuild_button_points_at_the_default_panel(self):
        request = self.factory.get(ADMIN_PANEL)
        request.resolver_match = django_urls.resolve(ADMIN_PANEL)
        request.user = self.request.user
        request.session = self.request.session
        server = self.servers.first()
        action = tables.RebuildInstance()
        action.table = admin_tables.AdminInstancesTable(request)

        self.assertEqual(DEFAULT_PANEL + "%s/rebuild" % server.id,
                         action.get_link_url(server))
