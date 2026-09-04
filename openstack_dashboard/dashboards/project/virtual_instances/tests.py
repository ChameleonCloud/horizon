import types

from django.urls import reverse

from horizon.test import helpers as horizon_helpers

from openstack_dashboard import api
from openstack_dashboard.dashboards.project.instances import tables
from openstack_dashboard.dashboards.project.virtual_instances import tables \
    as virtual_tables
from openstack_dashboard.test import helpers


INDEX_URL = reverse("horizon:project:virtual_instances:index")


def _url(action, *args):
    return reverse(
        "horizon:project:virtual_instances:%s" % action, args=args)


@horizon_helpers.pytest_mark("hybrid_site")
class VirtualPanelTestCase(helpers.TestCase):
    def setUp(self):
        super().setUp()
        self.server = self.servers.first()

    def _assert_returns_to_index(self, res):
        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, INDEX_URL)

    def _assert_form_posts_to(self, res, url):
        self.assertContains(res, 'action="%s"' % url)

    def _mock_image_choices(self):
        self.mock_image_list_detailed.return_value = \
            [self.images.list(), False, False]

    def _mock_disassociate_choices(self):
        port = next(p for p in self.ports.list()
                    if p.device_id == self.server.id)
        fip = self.floating_ips.first()
        fip.port_id = port.id
        self.mock_floating_ip_target_list_by_instance.return_value = [
            api.neutron.FloatingIpTarget(
                port, port["fixed_ips"][0]["ip_address"], self.server.name)]
        self.mock_tenant_floating_ip_list.return_value = [fip]
        return fip


class LaunchButtonUrlTests(VirtualPanelTestCase):
    """The launch button's destination and wizard flow.

    Test that the angular wizard button opens the right wizard, with urls
    directing to the virtual panel on success.
    """

    def _ng_click(self):
        action = tables.LaunchVirtualInstanceLinkNG()
        action.table = virtual_tables.VirtualInstancesTable(self.request)
        action.get_default_attrs()
        return action.attrs["ng-click"]

    def test_launch_wizard_returns_to_the_virtual_panel(self):
        self.assertIn("successUrl: '%s'" % INDEX_URL, self._ng_click())

    def test_launch_wizard_opens_the_virtual_flow(self):
        self.assertIn("instanceType: 'virtual'", self._ng_click())


class ModalFormViewSuccessUrlTests(VirtualPanelTestCase):
    """Test instance actions which use ModalFormView.

    On success, each one redirects to `success_url`.
    """

    @helpers.create_mocks({api.neutron: ("port_list",),
                           api.nova: ("interface_detach",)})
    def test_detach_interface_returns_to_the_virtual_panel(self):
        port = self.ports.first()
        self.mock_port_list.return_value = [port]
        self.mock_interface_detach.return_value = None

        res = self.client.post(
            _url("detach_interface", self.server.id),
            {"instance_id": self.server.id, "port": port.id})

        self._assert_returns_to_index(res)

    @helpers.create_mocks({api.neutron: ("network_list_for_tenant",
                                         "port_list_with_trunk_types"),
                           api.nova: ("interface_attach",)})
    def test_attach_interface_returns_to_the_virtual_panel(self):
        network = self.networks.first()
        self.mock_network_list_for_tenant.return_value = [network]
        self.mock_port_list_with_trunk_types.return_value = self.ports.list()
        self.mock_interface_attach.return_value = None

        res = self.client.post(
            _url("attach_interface", self.server.id),
            {"instance_id": self.server.id,
             "specification_method": "network",
             "network": network.id,
             "fixed_ip": "10.0.0.10"})

        self._assert_returns_to_index(res)

    @helpers.create_mocks({api.nova: ("instance_volumes_list",
                                      "instance_volume_detach")})
    def test_detach_volume_returns_to_the_virtual_panel(self):
        volume = self.cinder_volumes.list()[1]
        self.mock_instance_volumes_list.return_value = \
            self.cinder_volumes.list()
        self.mock_instance_volume_detach.return_value = None

        res = self.client.post(
            _url("detach_volume", self.server.id),
            {"volume": volume.id, "instance_id": self.server.id})

        self._assert_returns_to_index(res)

    @helpers.create_mocks({api.nova: ("instance_volume_attach",),
                           api.cinder: ("volume_list",)})
    def test_attach_volume_returns_to_the_virtual_panel(self):
        volume = self.cinder_volumes.list()[1]
        self.mock_volume_list.return_value = self.cinder_volumes.list()
        self.mock_instance_volume_attach.return_value = \
            types.SimpleNamespace(device="/dev/vdb")

        res = self.client.post(
            _url("attach_volume", self.server.id),
            {"volume": volume.id, "instance_id": self.server.id})

        self._assert_returns_to_index(res)

    @helpers.create_mocks({api.nova: ("server_rescue",),
                           api.glance: ("image_list_detailed",)})
    def test_rescue_returns_to_the_virtual_panel(self):
        self._mock_image_choices()
        self.mock_server_rescue.return_value = []

        res = self.client.post(
            _url("rescue", self.server.id),
            {"instance_id": self.server.id,
             "image": self.images.first().id})

        self._assert_returns_to_index(res)

    @helpers.create_mocks({api.nova: ("server_get", "server_rebuild",
                                      "is_feature_available"),
                           api.glance: ("image_list_detailed",)})
    def test_rebuild_returns_to_the_virtual_panel(self):
        self._mock_image_choices()
        self.mock_server_get.return_value = self.server
        self.mock_server_rebuild.return_value = []
        self.mock_is_feature_available.return_value = False

        res = self.client.post(
            _url("rebuild", self.server.id),
            {"instance_id": self.server.id,
             "image": self.images.first().id})

        self._assert_returns_to_index(res)

    @helpers.create_mocks({api.neutron: ("floating_ip_target_list_by_instance",
                                         "tenant_floating_ip_list",
                                         "floating_ip_disassociate")})
    def test_disassociate_returns_to_the_virtual_panel(self):
        fip = self._mock_disassociate_choices()
        self.mock_floating_ip_disassociate.return_value = None

        res = self.client.post(_url("disassociate", self.server.id),
                               {"fip": fip.id, "is_release": False})

        self._assert_returns_to_index(res)


class ModalFormViewSubmitUrlTests(VirtualPanelTestCase):
    """Test where an instance action's modal form posts.

    These templates have no form_action block, so the rendered action
    comes from submit_url. If it names the default panel the browser
    posts there, reaching that panel's view and its success_url.
    """

    @helpers.create_mocks({api.neutron: ("port_list",)})
    def test_detach_interface_form_posts_to_the_virtual_panel(self):
        self.mock_port_list.return_value = [self.ports.first()]
        url = _url("detach_interface", self.server.id)

        res = self.client.get(url)

        self._assert_form_posts_to(res, url)

    @helpers.create_mocks({api.neutron: ("network_list_for_tenant",
                                         "port_list_with_trunk_types")})
    def test_attach_interface_form_posts_to_the_virtual_panel(self):
        self.mock_network_list_for_tenant.return_value = \
            [self.networks.first()]
        self.mock_port_list_with_trunk_types.return_value = self.ports.list()
        url = _url("attach_interface", self.server.id)

        res = self.client.get(url)

        self._assert_form_posts_to(res, url)

    @helpers.create_mocks({api.nova: ("instance_volumes_list",)})
    def test_detach_volume_form_posts_to_the_virtual_panel(self):
        self.mock_instance_volumes_list.return_value = \
            self.cinder_volumes.list()
        url = _url("detach_volume", self.server.id)

        res = self.client.get(url)

        self._assert_form_posts_to(res, url)

    @helpers.create_mocks({api.cinder: ("volume_list",)})
    def test_attach_volume_form_posts_to_the_virtual_panel(self):
        self.mock_volume_list.return_value = self.cinder_volumes.list()
        url = _url("attach_volume", self.server.id)

        res = self.client.get(url)

        self._assert_form_posts_to(res, url)


class WorkflowSuccessUrlTests(VirtualPanelTestCase):
    """Test instance actions which use WorkflowView.

    Workflows accept a "next" parameter. When the POST omits it they
    fall back to success_url, so both cases are tested.
    """

    def _prepare_update(self):
        self.mock_server_get.return_value = self.server
        self.mock_is_feature_available.return_value = False
        self.mock_security_group_list.return_value = \
            self.security_groups.list()[:3]
        self.mock_server_security_groups.return_value = \
            self.security_groups.list()[:2]
        self.mock_server_update.return_value = self.server
        self.mock_server_update_security_groups.return_value = None
        return {"name": self.server.name}

    def _prepare_resize(self):
        self.mock_server_get.return_value = self.server
        self.mock_flavor_list.return_value = self.flavors.list()
        self.mock_server_resize.return_value = []
        flavor = next(f for f in self.flavors.list()
                      if f.id != self.server.flavor["id"])
        return {"flavor": flavor.id, "disk_config": "AUTO"}

    @helpers.create_mocks({api.nova: ("server_get", "server_update",
                                      "is_feature_available"),
                           api.neutron: ("security_group_list",
                                         "server_security_groups",
                                         "server_update_security_groups")})
    def test_update_without_next_returns_to_the_virtual_panel(self):
        res = self.client.post(_url("update", self.server.id),
                               self._prepare_update())

        self._assert_returns_to_index(res)

    @helpers.create_mocks({api.nova: ("server_get", "server_update",
                                      "is_feature_available"),
                           api.neutron: ("security_group_list",
                                         "server_security_groups",
                                         "server_update_security_groups")})
    def test_update_with_next_returns_to_the_virtual_panel(self):
        form_data = dict(self._prepare_update(), next=INDEX_URL)

        res = self.client.post(_url("update", self.server.id), form_data)

        self._assert_returns_to_index(res)

    @helpers.create_mocks({api.nova: ("server_get", "server_resize",
                                      "flavor_list")})
    def test_resize_without_next_returns_to_the_virtual_panel(self):
        res = self.client.post(_url("resize", self.server.id),
                               self._prepare_resize())

        self._assert_returns_to_index(res)

    @helpers.create_mocks({api.nova: ("server_get", "server_resize",
                                      "flavor_list")})
    def test_resize_with_next_returns_to_the_virtual_panel(self):
        form_data = dict(self._prepare_resize(), next=INDEX_URL)

        res = self.client.post(_url("resize", self.server.id), form_data)

        self._assert_returns_to_index(res)


class ModalTemplateUrlTests(VirtualPanelTestCase):
    """Test instance actions whose template writes its own urls.

    These templates set form_action with a {% url %} tag, so submit_url
    never reaches them. Both panels render the same template file, and a
    {% url %} tag names a route literally, so the url cannot differ
    between them. Therefore fixing these needs a per-panel template, or
    a url passed in from the view.
    """

    @helpers.create_mocks({api.nova: ("get_password",)})
    def test_decrypt_password_form_posts_back_to_the_virtual_panel(self):
        self.mock_get_password.return_value = "azerty"
        url = _url("decryptpassword", self.server.id, self.server.key_name)

        res = self.client.get(url)

        self.assertContains(res, 'action="%s" method="POST"' % url)

    @helpers.create_mocks({api.nova: ("get_password",)})
    def test_decrypt_password_cancel_returns_to_the_virtual_panel(self):
        self.mock_get_password.return_value = "azerty"
        url = _url("decryptpassword", self.server.id, self.server.key_name)

        res = self.client.get(url)

        self.assertContains(
            res, '<a href="%s" class="btn btn-default cancel">' % INDEX_URL)

    @helpers.create_mocks({api.glance: ("image_list_detailed",)})
    def test_rescue_form_posts_back_to_the_virtual_panel(self):
        self._mock_image_choices()
        url = _url("rescue", self.server.id)

        res = self.client.get(url)

        self._assert_form_posts_to(res, url)

    @helpers.create_mocks({api.glance: ("image_list_detailed",),
                           api.nova: ("server_get", "is_feature_available")})
    def test_rebuild_form_posts_back_to_the_virtual_panel(self):
        self._mock_image_choices()
        self.mock_server_get.return_value = self.server
        self.mock_is_feature_available.return_value = False
        url = _url("rebuild", self.server.id)

        res = self.client.get(url)

        self._assert_form_posts_to(res, url)

    @helpers.create_mocks({api.neutron: (
        "floating_ip_target_list_by_instance", "tenant_floating_ip_list")})
    def test_disassociate_form_posts_back_to_the_virtual_panel(self):
        self._mock_disassociate_choices()
        url = _url("disassociate", self.server.id)

        res = self.client.get(url)

        self._assert_form_posts_to(res, url)
