from django.urls import re_path
from django.utils.translation import gettext_lazy as _

from openstack_dashboard.dashboards.project.key_pairs import views as legacy_views

urlpatterns = [
    re_path(r'^$', legacy_views.IndexView.as_view(), name='index'),
    re_path(r'^import/$', legacy_views.ImportView.as_view(), name='import'),
    re_path(r'^(?P<keypair_name>[^/]+)/$',
            legacy_views.DetailView.as_view(),
            name='detail'),
]
