from django.utils.translation import gettext_lazy as _

# The slug of the panel group to be added to HORIZON_CONFIG. Required.
PANEL_GROUP = 'virtual_compute'
# The display name of the PANEL_GROUP. Required.
PANEL_GROUP_NAME = _('Virtual Machines')
# The slug of the dashboard the PANEL_GROUP associated with. Required.
PANEL_GROUP_DASHBOARD = 'project'

# CHI: registered unconditionally, and deliberately so. The panels in it gate
# themselves on CHAMELEON_ENABLE_VMS via can_register(), and _sidebar.html
# wraps the group heading in `{% if filtered_panels %}`, so a baremetal-only
# site renders no heading for an empty group.
#
# Do not add `DISABLED = not settings.CHAMELEON_ENABLE_VMS` here. Reading
# django.conf.settings in this directory snapshots a half-built settings
# module: update_dashboards() runs at openstack_dashboard/settings.py:349,
# while HORIZON_COMPRESS_OFFLINE_CONTEXT_BASE is not defined until :368.
