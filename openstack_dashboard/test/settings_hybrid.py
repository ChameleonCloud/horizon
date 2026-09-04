"""Test settings for a hybrid baremetal + VM site.

This file exists in order to test CHI custom panels which use can_register()
to enable only when CHAMELEON_ENABLE_VMS=True. can_register() is evaluated
at startup, and cannot be overridden via per-test overrides.

In order to keep upstream tests pasing, we can't override the value in
openstack_dashboard.test.settings.py.
"""

from openstack_dashboard.test.settings import *  # noqa: F401,F403,H303

CHAMELEON_ENABLE_VMS = True
