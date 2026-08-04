PANEL_DASHBOARD = 'project'
PANEL_GROUP = 'network'
PANEL = 'security_groups'

from django.conf import settings
if not settings.CHAMELEON_BAREMETAL_ONLY:
    ADD_PANEL = ('openstack_dashboard.dashboards.project.security_groups'
                '.panel.SecurityGroups')
