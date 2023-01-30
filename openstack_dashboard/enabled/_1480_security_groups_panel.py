from django.conf import settings

PANEL_DASHBOARD = 'project'
PANEL_GROUP = 'network'
PANEL = 'security_groups'

# Security groups don't work on bare metal sites, so we don't load them there
# ADD_PANEL = ('openstack_dashboard.dashboards.project.security_groups'
#              '.panel.SecurityGroups')
