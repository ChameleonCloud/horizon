from django.conf.urls import include
from django.urls import re_path
from django.utils.translation import gettext_lazy as _

from openstack_dashboard.dashboards.project.instances import views
from openstack_dashboard.dashboards.project.instances import urls as instance_urls

urlpatterns = [
    re_path(r'^$', views.VirtualIndexView.as_view(), name='index'),
    re_path(r'', include((instance_urls, 'instances'))),
]
