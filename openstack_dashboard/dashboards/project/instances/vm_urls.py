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

"""URLconf for the "Virtual Compute" instances panel.

Only the index view differs from urls.py; every detail and action route
is the shared one, included here so that a URL under this panel's prefix
still resolves.

The index route is deliberately built here with a fresh re_path() rather
than reused from urls.py: horizon.base._decorate_urlconf() rewrites
URLPattern.callback in place, and urls.py's urlpatterns is a single
module-level list shared with the baremetal panel. A shared pattern
would end up owned by whichever panel horizon decorated first, and the
sidebar would highlight the wrong entry.
"""

from django.conf.urls import include
from django.urls import re_path

from openstack_dashboard.dashboards.project.instances \
    import urls as instance_urls
from openstack_dashboard.dashboards.project.instances import views


urlpatterns = [
    re_path(r'^$', views.VirtualIndexView.as_view(), name='index'),
    re_path(r'', include((instance_urls, 'instances'))),
]
