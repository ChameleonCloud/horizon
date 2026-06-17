from django.conf.urls import include
from django.urls import re_path
from django.utils.translation import gettext_lazy as _

from openstack_dashboard.dashboards.project.images import views
from openstack_dashboard.dashboards.project.images.images import urls as image_urls
from openstack_dashboard.dashboards.project.images.snapshots import urls as snapshot_urls

urlpatterns = [
    re_path(r'^$', views.VirtualIndexView.as_view(), name='index'),
    re_path(r'', include((image_urls, 'images'))),
    re_path(r'', include((snapshot_urls, 'snapshots'))),
]
