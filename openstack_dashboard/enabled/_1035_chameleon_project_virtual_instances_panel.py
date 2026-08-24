# The slug of the panel to be added to HORIZON_CONFIG. Required.
PANEL = 'instances_virtual'
# The slug of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = 'project'
# The slug of the panel group the PANEL is associated with.
PANEL_GROUP = 'virtual_compute'

# Python panel class of the PANEL to be added. The class gates itself on
# CHAMELEON_ENABLE_VMS via can_register().
ADD_PANEL = ('openstack_dashboard.dashboards.project.instances'
             '.panel.VirtualInstances')
