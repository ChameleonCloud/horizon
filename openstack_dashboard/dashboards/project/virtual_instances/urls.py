from django.conf.urls import include
from django.urls import re_path

from openstack_dashboard.dashboards.project.instances import urls \
    as instance_urls
from openstack_dashboard.dashboards.project.virtual_instances import views


urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(
            r"^(?P<instance_id>[^/]+)/$",
            views.DetailView.as_view(),
            name="detail",
        ),
    # included from default urlconf to about large copy+paste. Tradeoff:
    # They are nested as virtual_instances:instances:<name>
    # TODO(Mike): Flatten the nesting to avoid extra :instances:
    # When flattening, be sure to drop "detail" from above to avoid conflict.
    re_path(r'', include((instance_urls, 'instances'))),
]
