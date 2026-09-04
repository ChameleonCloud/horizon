PANEL_DASHBOARD = 'project'
# TODO(Mike): Make configurable
# security groups must be disabled if CHAMELEON_ENABLE_VMS is false.
PANEL_GROUP = 'virtual_compute'
PANEL = 'security_groups'

ADD_PANEL = ('openstack_dashboard.dashboards.project.security_groups'
             '.panel.SecurityGroups')
