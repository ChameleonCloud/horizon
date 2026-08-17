from django.utils.translation import gettext_lazy as _

# The slug of the panel group to be added to HORIZON_CONFIG. Required.
PANEL_GROUP = 'compute'
# The display name of the PANEL_GROUP. Required.
# CHI: named for what it holds, so that a hybrid site's "Virtual Compute"
# group reads as its counterpart. The slug stays 'compute' -- renaming it would
# move every panel in the group.
PANEL_GROUP_NAME = _('Baremetal Compute')
# The slug of the dashboard the PANEL_GROUP associated with. Required.
PANEL_GROUP_DASHBOARD = 'project'
