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

Do not include() urls.py here. _decorate_urlconf() rewrites
URLPattern.callback in place, so mounting that shared list under a second panel
hands its routes to whichever panel horizon decorated last.
"""

from django.urls import re_path

from openstack_dashboard.dashboards.project.instances import views


urlpatterns = [
    re_path(r'^$', views.VirtualIndexView.as_view(), name='index'),
]
