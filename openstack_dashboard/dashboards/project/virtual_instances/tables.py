from django.utils.translation import gettext_lazy as _

from openstack_dashboard.dashboards.project.instances import tables


class VirtualInstancesTable(tables.InstancesTable):
    class Meta(tables.InstancesTable.Meta):
        name = "virtual_instances"
        verbose_name = _("Virtual Instances")
        launch_actions = (tables.LaunchVirtualInstanceLinkNG,)
        table_actions = launch_actions + (tables.DeleteInstance,
                                          tables.InstancesFilterAction)
