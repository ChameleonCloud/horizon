# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.conf import settings
from django.template.defaultfilters import floatformat
from django import urls
from django.utils.translation import gettext_lazy as _

from horizon import tables
from horizon.templatetags import sizeformat
from horizon.utils import filters


# Per-instance usage columns, vcpus, disk, and memory are not meaningful for
# chameleon baremetal, all set to 1,0,0 to skip nova scheduling.
BAREMETAL_HIDDEN_USAGE_COLUMNS = frozenset(["vcpus", "disk", "memory"])


class CSVSummary(tables.LinkAction):
    name = "csv_summary"
    verbose_name = _("Download CSV Summary")
    icon = "download"

    def get_link_url(self, usage=None):
        return self.table.kwargs['usage'].csv_link()


class BaseUsageTable(tables.DataTable):
    vcpus = tables.Column('vcpus', verbose_name=_("VCPUs"))
    disk = tables.Column('local_gb', verbose_name=_("Disk"),
                         filters=(sizeformat.diskgbformat,),
                         attrs={"data-type": "size"})
    memory = tables.Column('memory_mb',
                           verbose_name=_("RAM"),
                           filters=(sizeformat.mb_float_format,),
                           attrs={"data-type": "size"})


class GlobalUsageTable(BaseUsageTable):
    project = tables.Column('project_name', verbose_name=_("Project Name"))
    vcpu_hours = tables.Column('vcpu_hours', verbose_name=_("VCPU Hours"),
                               help_text=_("Total VCPU usage (Number of "
                                           "VCPU in instance * Hours Used) "
                                           "for the project"),
                               filters=(lambda v: floatformat(v, 2),))
    disk_hours = tables.Column('disk_gb_hours',
                               verbose_name=_("Disk GB Hours"),
                               help_text=_("Total disk usage (GB * "
                                           "Hours Used) for the project"),
                               filters=(lambda v: floatformat(v, 2),))
    memory_hours = tables.Column('memory_mb_hours',
                                 verbose_name=_("Memory MB Hours"),
                                 help_text=_("Total memory usage (MB * "
                                             "Hours Used) for the project"),
                                 filters=(lambda v: floatformat(v, 2),))

    def get_object_id(self, datum):
        return datum.tenant_id

    class Meta(object):
        name = "global_usage"
        hidden_title = False
        verbose_name = _("Usage")
        columns = ("project", "vcpus", "disk", "memory",
                   "vcpu_hours", "disk_hours", "memory_hours")
        table_actions = (CSVSummary,)
        multi_select = False


def get_instance_link(datum):
    view = "horizon:project:instances:detail"
    if datum.get('instance_id', False):
        return urls.reverse(view, args=(datum.get('instance_id'),))
    return None


class ProjectUsageTable(BaseUsageTable):
    instance = tables.Column('name',
                             verbose_name=_("Instance Name"),
                             link=get_instance_link)
    uptime = tables.Column('uptime_at',
                           verbose_name=_("Age"),
                           filters=(filters.timesince_sortable,),
                           attrs={'data-type': 'timesince'})

    def get_object_id(self, datum):
        return datum.get('instance_id', id(datum))

    def get_columns(self):
        columns = super().get_columns()
        if settings.CHAMELEON_ENABLE_BAREMETAL:
            return [
                c
                for c in columns
                if c.name not in BAREMETAL_HIDDEN_USAGE_COLUMNS
            ]
        return columns

    class Meta(object):
        name = "project_usage"
        hidden_title = False
        verbose_name = _("Usage")
        columns = ("instance", "vcpus", "disk", "memory", "uptime")
        table_actions = (CSVSummary,)
        multi_select = False
