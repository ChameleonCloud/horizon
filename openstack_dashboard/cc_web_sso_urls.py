from django import shortcuts
from django.conf import settings
from django.conf.urls import url

from openstack_auth import utils


def force_password_login(request):
    login_url = request.build_absolute_uri(settings.LOGIN_URL)
    return shortcuts.redirect(utils.url_query_append(login_url, {
        utils.FORCE_OLD_LOGIN_EXPERIENCE_PARAM: '1'
    }))


urlpatterns = []

if utils.is_websso_enabled():
    urlpatterns += [
        url(r"^force-password-login$", force_password_login, name='chameleon_force_password_login'),
    ]
