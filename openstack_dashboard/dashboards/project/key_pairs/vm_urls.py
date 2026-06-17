from django.urls import re_path
from django.utils.translation import gettext_lazy as _

from horizon.browsers import views
from openstack_dashboard.dashboards.project.key_pairs import views as legacy_views
from openstack_dashboard.utils import settings as setting_utils

# Guard against missing ANGULAR_FEATURES keys in defaults/settings
use_angular = False
try:
    use_angular = bool(setting_utils.get_dict_config('ANGULAR_FEATURES', 'key_pairs_panel'))
except KeyError:
    use_angular = False

if use_angular:
    title = _("Key Pairs")
    urlpatterns = [
        re_path('', views.AngularIndexView.as_view(title=title), name='index'),
        re_path(r'^(?P<keypair_name>[^/]+)/$',
                views.AngularIndexView.as_view(title=title),
                name='detail'),
    ]
else:
    urlpatterns = [
        re_path(r'^$', legacy_views.BaremetalIndexView.as_view(), name='index'),
        re_path(r'^import/$', legacy_views.ImportView.as_view(), name='import'),
        re_path(r'^(?P<keypair_name>[^/]+)/$',
                legacy_views.DetailView.as_view(),
                name='detail'),
    ]
