from openstack_dashboard.dashboards.project.instances import workflows


# A route name, not a path: Workflow.get_success_url reverses it.
SUCCESS_URL = "horizon:project:virtual_instances:index"


class UpdateInstance(workflows.UpdateInstance):
    success_url = SUCCESS_URL


class ResizeInstance(workflows.ResizeInstance):
    success_url = SUCCESS_URL
