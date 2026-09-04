from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from openstack_dashboard.dashboards.project.instances import views
from openstack_dashboard.dashboards.project.virtual_instances import tables


class IndexView(views.IndexView):
    table_class = tables.VirtualInstancesTable
    page_title = _("Virtual Instances")
    baremetal = False


class DetailView(views.DetailView):
    # List page, user sent here when instance not found.
    redirect_url = 'horizon:project:virtual_instances:index'

    # This view is for the virtual compute panel.
    baremetal = False


INDEX_URL = reverse_lazy("horizon:project:virtual_instances:index")


class RescueView(views.RescueView):
    submit_url = "horizon:project:virtual_instances:rescue"
    success_url = INDEX_URL


class RebuildView(views.RebuildView):
    success_url = INDEX_URL


class DisassociateView(views.DisassociateView):
    success_url = INDEX_URL


class AttachInterfaceView(views.AttachInterfaceView):
    success_url = INDEX_URL


class DetachInterfaceView(views.DetachInterfaceView):
    success_url = INDEX_URL


class AttachVolumeView(views.AttachVolumeView):
    success_url = INDEX_URL


class DetachVolumeView(views.DetachVolumeView):
    success_url = INDEX_URL
