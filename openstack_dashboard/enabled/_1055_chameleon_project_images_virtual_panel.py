# The slug of the panel to be added to HORIZON_CONFIG. Required.
PANEL = 'virtual_images'
# The slug of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = 'project'
# The slug of the panel group the PANEL is associated with.
PANEL_GROUP = 'virtual_compute'

# Python panel class of the PANEL to be added.
from django.conf import settings
if settings.CHAMELEON_ENABLE_VMS:
    ADD_PANEL = 'openstack_dashboard.dashboards.project.images.panel.VirtualImages'
