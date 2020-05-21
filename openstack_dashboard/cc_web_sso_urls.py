from django.conf import settings
from django.conf.urls import url
from django import http as django_http

from openstack_auth import utils
from openstack_auth import views


def request_new_login(request):
    res = django_http.HttpResponseRedirect(settings.LOGIN_URL)
    res.set_cookie(utils.FORCE_WEBSSO_CHOICES_COOKIE, '1', max_age=60*60*24)
    return res


urlpatterns = []

# TODO: remove this extra URL for websso when Portal is updated to just use
# the "built-in" URL in Horizon (/websso)
if utils.is_websso_enabled():
    urlpatterns += [
        url(r"^ccwebsso/$", views.websso, name='chameleon_websso'),
        url(r"^new-login-flow/$", request_new_login, name='chameleon_new_login'),
    ]
