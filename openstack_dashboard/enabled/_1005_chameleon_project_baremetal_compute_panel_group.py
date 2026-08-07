from django.conf import settings
from django.utils.translation import gettext_lazy as _

# The slug of the panel group to be added to HORIZON_CONFIG. Required.
PANEL_GROUP = 'baremetal_compute'
# The display name of the PANEL_GROUP. Required.

# CHI: If VMs will run alongisde baremetal, rename compute -> baremetal compute.
PANEL_GROUP_NAME = (
    _("Baremetal Compute") if settings.CHAMELEON_ENABLE_VMS else _("Compute")
)
# The slug of the dashboard the PANEL_GROUP associated with. Required.
PANEL_GROUP_DASHBOARD = 'project'
