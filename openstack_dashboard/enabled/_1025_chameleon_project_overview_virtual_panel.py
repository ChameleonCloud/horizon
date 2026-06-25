PANEL = 'overview_virtual'
PANEL_DASHBOARD = 'project'
PANEL_GROUP = 'virtual_compute'


from django.conf import settings
if settings.CHAMELEON_ENABLE_VMS:
    ADD_PANEL = 'openstack_dashboard.dashboards.project.overview.panel.VirtualOverview'
