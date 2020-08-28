from django.conf.urls import url

from openstack_auth import utils
from openstack_auth import views


urlpatterns = []

# TODO: remove this extra URL for websso when Portal is updated to just use
# the "built-in" URL in Horizon (/websso)
if utils.is_websso_enabled():
    urlpatterns += [
        url(r"^ccwebsso/$", views.websso, name='chameleon_websso'),
    ]
