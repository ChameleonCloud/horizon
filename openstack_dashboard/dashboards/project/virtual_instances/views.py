from django.utils.translation import gettext_lazy as _

from openstack_dashboard.dashboards.project.instances import views
from openstack_dashboard.dashboards.project.virtual_instances import tables


class IndexView(views.IndexView):
    table_class = tables.VirtualInstancesTable
    page_title = _("Virtual Instances")
    baremetal = False


class DetailView(views.DetailView):
    # This view is for the virtual compute panel.
    baremetal = False


# Served unchanged from the default compute panel. Listing them means a
# view added there but not considered here fails at startup, rather than
# leaving this panel a route short.
AttachInterfaceView = views.AttachInterfaceView
AttachVolumeView = views.AttachVolumeView
DecryptPasswordView = views.DecryptPasswordView
DetachInterfaceView = views.DetachInterfaceView
DetachVolumeView = views.DetachVolumeView
DisassociateView = views.DisassociateView
RebuildView = views.RebuildView
RescueView = views.RescueView
ResizeView = views.ResizeView
SerialConsoleView = views.SerialConsoleView
UpdatePortView = views.UpdatePortView
UpdateView = views.UpdateView
auto_console = views.auto_console
console = views.console
rdp = views.rdp
spice = views.spice
vnc = views.vnc
