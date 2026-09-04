from django.urls import re_path

from openstack_dashboard.dashboards.project.instances import (
    views as instance_views,
)
from openstack_dashboard.dashboards.project.virtual_instances import views

INSTANCES = r"^(?P<instance_id>[^/]+)/%s$"
INSTANCES_KEYPAIR = r"^(?P<instance_id>[^/]+)/(?P<keypair_name>[^/]+)/%s$"

urlpatterns = [
    re_path(r"^$", views.IndexView.as_view(), name="index"),
    re_path(
        r"^(?P<instance_id>[^/]+)/$", views.DetailView.as_view(), name="detail"
    ),
    re_path(
        INSTANCES % "update",
        views.UpdateView.as_view(),
        name="update",
    ),
    re_path(
        INSTANCES % "rebuild",
        views.RebuildView.as_view(),
        name="rebuild",
    ),
    re_path(
        INSTANCES % "serial",
        instance_views.SerialConsoleView.as_view(),
        name="serial",
    ),
    re_path(INSTANCES % "console", instance_views.console, name="console"),
    re_path(
        INSTANCES % "auto_console",
        instance_views.auto_console,
        name="auto_console",
    ),
    re_path(INSTANCES % "vnc", instance_views.vnc, name="vnc"),
    re_path(INSTANCES % "spice", instance_views.spice, name="spice"),
    re_path(INSTANCES % "rdp", instance_views.rdp, name="rdp"),
    re_path(
        INSTANCES % "resize",
        views.ResizeView.as_view(),
        name="resize",
    ),
    re_path(
        INSTANCES_KEYPAIR % "decryptpassword",
        views.DecryptPasswordView.as_view(),
        name="decryptpassword",
    ),
    re_path(
        INSTANCES % "disassociate",
        views.DisassociateView.as_view(),
        name="disassociate",
    ),
    re_path(
        INSTANCES % "attach_interface",
        views.AttachInterfaceView.as_view(),
        name="attach_interface",
    ),
    re_path(
        INSTANCES % "detach_interface",
        views.DetachInterfaceView.as_view(),
        name="detach_interface",
    ),
    re_path(
        r"^(?P<instance_id>[^/]+)/attach_volume/$",
        views.AttachVolumeView.as_view(),
        name="attach_volume",
    ),
    re_path(
        r"^(?P<instance_id>[^/]+)/detach_volume/$",
        views.DetachVolumeView.as_view(),
        name="detach_volume",
    ),
    re_path(
        r"^(?P<instance_id>[^/]+)/ports/(?P<port_id>[^/]+)/update$",
        instance_views.UpdatePortView.as_view(),
        name="update_port",
    ),
    re_path(INSTANCES % "rescue", views.RescueView.as_view(), name="rescue"),
]
