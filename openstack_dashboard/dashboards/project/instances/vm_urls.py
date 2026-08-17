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

"""CHI: URLs for the virtual instances panel.

A separate module rather than a reuse of urls.py: Panel._decorate_urlconf()
mutates the urlpatterns list in place, so two panels sharing one module would
double-wrap every view.

Only the index view is routed. Detail and per-instance action URLs stay in the
'instances' namespace, which the baremetal panel registers; routing them again
would give every one of them a second, ambiguous name.
"""

from django.urls import re_path

from openstack_dashboard.dashboards.project.instances import views


urlpatterns = [
    re_path(r'^$', views.VirtualIndexView.as_view(), name='index'),
]
