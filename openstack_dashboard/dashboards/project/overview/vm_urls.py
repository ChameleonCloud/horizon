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

"""URLconf for the "Virtual Compute" overview panel.

Identical to urls.py, but the routes are rebuilt here so that this panel
owns its own URLPattern objects; see instances/vm_urls.py for why that
matters.
"""

from django.urls import re_path

from openstack_dashboard.dashboards.project.overview import views


urlpatterns = [
    re_path(r'^$', views.ProjectOverview.as_view(), name='index'),
    re_path(r'^warning$', views.WarningView.as_view(), name='warning'),
]
