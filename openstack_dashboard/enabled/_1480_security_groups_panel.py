from django.conf import settings

PANEL_DASHBOARD = 'project'
PANEL_GROUP = 'network'
PANEL = 'security_groups'

# Security groups don't work on bare metal sites, so we don't load them there
if not settings.CHAMELEON_IS_BAREMETAL_SITE:
    ADD_PANEL = ('openstack_dashboard.dashboards.project.security_groups'
                 '.panel.SecurityGroups')
