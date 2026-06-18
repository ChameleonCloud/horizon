from django.urls import re_path
from django.utils.translation import gettext_lazy as _

from openstack_dashboard.dashboards.project.overview import views as overview_views

urlpatterns = [
    re_path(r'^$', overview_views.BaremetalIndexView.as_view(), name='index'),
]
