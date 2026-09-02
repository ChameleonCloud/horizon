from django.utils.translation import gettext_lazy as _

from openstack_dashboard.dashboards.project.instances import views


class IndexView(views.IndexView):
    page_title = _("Virtual Instances")
    baremetal = False
