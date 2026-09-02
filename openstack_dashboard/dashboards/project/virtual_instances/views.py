from django.utils.translation import gettext_lazy as _

from openstack_dashboard.dashboards.project.instances import views
from openstack_dashboard.dashboards.project.virtual_instances import tables


class IndexView(views.IndexView):
    table_class = tables.VirtualInstancesTable
    page_title = _("Virtual Instances")
    baremetal = False
