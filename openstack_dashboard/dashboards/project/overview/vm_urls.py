from django.urls import re_path
from django.utils.translation import gettext_lazy as _

from openstack_dashboard.dashboards.project.overview import views as overview_views
from openstack_dashboard.utils import settings as setting_utils

# Guard against missing ANGULAR_FEATURES keys in defaults/settings
use_angular = False
try:
    use_angular = bool(setting_utils.get_dict_config('ANGULAR_FEATURES', 'overview_panel'))
except KeyError:
    use_angular = False

if use_angular:
    title = _("Overview")
    urlpatterns = [
        re_path(r'^$', overview_views.BaremetalIndexView.as_view(title=title), name='index'),
    ]
else:
    urlpatterns = [
        re_path(r'^$', overview_views.BaremetalIndexView.as_view(), name='index'),
    ]
