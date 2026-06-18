PANEL = 'instances_virtual'
PANEL_DASHBOARD = 'project'
PANEL_GROUP = 'virtual_compute'

# Register a thin panel class that reuses instances.panel.Instances behavior
from django.conf import settings
if settings.CHAMELEON_ENABLE_VMS:
    ADD_PANEL = 'openstack_dashboard.dashboards.project.instances.panel.VirtualInstances'
