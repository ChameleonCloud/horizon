#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""URLconf for the "Virtual Compute" images panel.

Mirrors urls.py, including its ANGULAR_FEATURES branch, so the two
images panels behave identically. The index route is rebuilt here so
that this panel owns its own URLPattern object; see
instances/vm_urls.py for why that matters.
"""

from django.conf.urls import include
from django.urls import re_path
from django.utils.translation import gettext_lazy as _

from horizon.browsers.views import AngularIndexView
from openstack_dashboard.dashboards.project.images.images \
    import urls as image_urls
from openstack_dashboard.dashboards.project.images.snapshots \
    import urls as snapshot_urls
from openstack_dashboard.dashboards.project.images import views
from openstack_dashboard.utils import settings as setting_utils


if setting_utils.get_dict_config('ANGULAR_FEATURES', 'images_panel'):
    title = _("Images")
    index_view = AngularIndexView.as_view(title=title)
else:
    index_view = views.IndexView.as_view()

urlpatterns = [
    re_path(r'^$', index_view, name='index'),
    re_path(r'', include((image_urls, 'images'))),
    re_path(r'', include((snapshot_urls, 'snapshots'))),
]
