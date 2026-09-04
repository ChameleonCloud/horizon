from django.utils.translation import gettext_lazy as _

from horizon import tables as horizon_tables

from openstack_dashboard.dashboards.project.instances import tables
from openstack_dashboard.views import get_url_with_pagination


def get_server_detail_link(obj, request):
    return get_url_with_pagination(
        request,
        VirtualInstancesTable._meta.pagination_param,
        VirtualInstancesTable._meta.prev_pagination_param,
        "horizon:project:virtual_instances:detail",
        obj.id)


# Each of these inherits everything but the panel its url names.
class EditInstance(tables.EditInstance):
    url = "horizon:project:virtual_instances:update"


class EditInstanceSecurityGroups(tables.EditInstanceSecurityGroups):
    url = "horizon:project:virtual_instances:update"


class EditPortSecurityGroups(tables.EditPortSecurityGroups):
    url = "horizon:project:virtual_instances:detail"


class ConsoleLink(tables.ConsoleLink):
    url = "horizon:project:virtual_instances:detail"


class LogLink(tables.LogLink):
    url = "horizon:project:virtual_instances:detail"


class ResizeLink(tables.ResizeLink):
    url = "horizon:project:virtual_instances:resize"


class RebuildInstance(tables.RebuildInstance):
    url = "horizon:project:virtual_instances:rebuild"


class RescueInstance(tables.RescueInstance):
    url = "horizon:project:virtual_instances:rescue"


class DecryptInstancePassword(tables.DecryptInstancePassword):
    url = "horizon:project:virtual_instances:decryptpassword"


class DisassociateIP(tables.DisassociateIP):
    url = "horizon:project:virtual_instances:disassociate"


class AttachInterface(tables.AttachInterface):
    url = "horizon:project:virtual_instances:attach_interface"


class DetachInterface(tables.DetachInterface):
    url = "horizon:project:virtual_instances:detach_interface"


class AttachVolume(tables.AttachVolume):
    url = "horizon:project:virtual_instances:attach_volume"


class DetachVolume(tables.DetachVolume):
    url = "horizon:project:virtual_instances:detach_volume"


class VirtualInstancesTable(tables.InstancesTable):
    name = horizon_tables.WrappingColumn("name",
                                         link=get_server_detail_link,
                                         verbose_name=_("Instance Name"))

    class Meta(tables.InstancesTable.Meta):
        name = "virtual_instances"
        verbose_name = _("Virtual Instances")
        launch_actions = (tables.LaunchVirtualInstanceLinkNG,)
        table_actions = launch_actions + (tables.DeleteInstance,
                                          tables.InstancesFilterAction)
        row_actions = (
            tables.StartInstance,
            tables.ConfirmResize,
            tables.RevertResize,
            tables.CreateSnapshot,
            tables.AssociateIP,
            DisassociateIP,
            AttachInterface,
            DetachInterface,
            EditInstance,
            AttachVolume,
            DetachVolume,
            tables.UpdateMetadata,
            DecryptInstancePassword,
            EditInstanceSecurityGroups,
            EditPortSecurityGroups,
            ConsoleLink,
            LogLink,
            RescueInstance,
            tables.UnRescueInstance,
            tables.TogglePause,
            tables.ToggleSuspend,
            tables.ToggleShelve,
            ResizeLink,
            tables.LockInstance,
            tables.UnlockInstance,
            tables.SoftRebootInstance,
            tables.RebootInstance,
            tables.StopInstance,
            RebuildInstance,
            tables.DeleteInstance,
        )
