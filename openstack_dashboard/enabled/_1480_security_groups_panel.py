from django.conf import settings

PANEL_DASHBOARD = 'project'
PANEL_GROUP = 'network'
PANEL = 'security_groups'

# Security groups only work on KVM sites, so we only load them there
if settings.CHAMELEON_SITE_ID.startswith("KVM"):
    ADD_PANEL = ('openstack_dashboard.dashboards.project.security_groups'
                 '.panel.SecurityGroups')
