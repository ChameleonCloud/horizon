from django.urls import re_path

from openstack_dashboard.dashboards.project.virtual_instances import views


urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
]
