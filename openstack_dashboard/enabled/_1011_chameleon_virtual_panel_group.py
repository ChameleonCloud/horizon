from django.utils.translation import gettext_lazy as _

# The slug of the panel group to be added to HORIZON_CONFIG. Required.
PANEL_GROUP = 'virtual_compute'
# The display name of the PANEL_GROUP. Required.
PANEL_GROUP_NAME = _('Virtual Compute')
# The slug of the dashboard the PANEL_GROUP associated with. Required.
PANEL_GROUP_DASHBOARD = 'project'

# CHI: registered unconditionally. Its panels gate themselves on
# CHAMELEON_ENABLE_VMS via can_register(), and _sidebar.html hides a group with
# no visible panels.
#
# Do not gate this file on django.conf.settings: enabled/ modules are imported
# from update_dashboards(), part way through building the settings module, so
# settings read here are missing or half-built.
