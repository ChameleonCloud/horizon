PANEL = 'instances_virtual'
PANEL_DASHBOARD = 'project'
PANEL_GROUP = 'virtual_compute'

# Register a thin panel class that reuses instances.panel.Instances behavior
ADD_PANEL = 'openstack_dashboard.dashboards.project.instances.panel.VirtualInstances'
