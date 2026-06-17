PANEL_DASHBOARD = 'project'

# NOTE: Updated for Chameleon
PANEL_GROUP = 'virtual_compute'
PANEL = 'security_groups'

from django.conf import settings
if not settings.CHAMELEON_BAREMETAL_ONLY:
    ADD_PANEL = ('openstack_dashboard.dashboards.project.security_groups'
                '.panel.SecurityGroups')
