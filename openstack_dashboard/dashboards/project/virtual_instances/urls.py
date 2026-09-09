from openstack_dashboard.dashboards.project.instances import urls \
    as instance_urls
from openstack_dashboard.dashboards.project.virtual_instances import views

urlpatterns = instance_urls.new_instance_urlpatterns(views)
