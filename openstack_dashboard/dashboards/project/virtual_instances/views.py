from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from openstack_dashboard.dashboards.project.instances import views
from openstack_dashboard.dashboards.project.virtual_instances import tables
from openstack_dashboard.dashboards.project.virtual_instances import workflows


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


class UpdateView(views.UpdateView):
    workflow_class = workflows.UpdateInstance


class ResizeView(views.ResizeView):
    workflow_class = workflows.ResizeInstance


class RebuildView(views.RebuildView):
    success_url = INDEX_URL


class DisassociateView(views.DisassociateView):
    success_url = INDEX_URL


class _RepointedSubmitUrl:
    """HACK: override get_context_data so we can change the submit url used."""

    submit_url_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submit_url"] = reverse(
            self.submit_url_name,
            kwargs={"instance_id": self.kwargs["instance_id"]})
        return context


class AttachInterfaceView(_RepointedSubmitUrl, views.AttachInterfaceView):
    submit_url_name = "horizon:project:virtual_instances:attach_interface"
    success_url = INDEX_URL


class DetachInterfaceView(_RepointedSubmitUrl, views.DetachInterfaceView):
    submit_url_name = "horizon:project:virtual_instances:detach_interface"
    success_url = INDEX_URL


class AttachVolumeView(_RepointedSubmitUrl, views.AttachVolumeView):
    submit_url_name = "horizon:project:virtual_instances:attach_volume"
    success_url = INDEX_URL


class DetachVolumeView(_RepointedSubmitUrl, views.DetachVolumeView):
    submit_url_name = "horizon:project:virtual_instances:detach_volume"
    success_url = INDEX_URL
