# Copyright 2016 OpenStack Foundation
# All Rights Reserved.
#
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

from webob import exc
from oslo_log import log as logging

from nova.api.openstack import api_version_request
from nova.api.openstack import common
from nova.api.openstack.compute.schemas import server_volume_qos
from nova.api.openstack import wsgi
from nova.api import validation
from nova.compute import api as compute
from nova.compute import vm_states
from nova import exception
from nova.i18n import _
#from nova.policies import servers_migrations as sm_policies

LOG = logging.getLogger(__name__)


class ServerVolumeQosController(wsgi.Controller):
    """The server migrations API controller for the OpenStack API."""

    def __init__(self):
        super(ServerVolumeQosController, self).__init__()
        self.compute_api = compute.API()

    @wsgi.Controller.api_version("2.1")
    @wsgi.expected_errors((404, 409))
    def index(self, req, server_id):
        """Return all migrations of an instance in progress."""
        context = req.environ['nova.context']
        #context.can(sm_policies.POLICY_ROOT % 'index')

        instance = common.get_instance(self.compute_api, context, server_id)
        if instance.vm_state != vm_states.ACTIVE:
            raise exc.HTTPConflict(
                explanation="Instance %s current stats is %s not ACTIVE." %
                (server_id, instance.vm_state))
        LOG.debug("query qos of instance: %s", instance.id)
        qos_config = self.compute_api.get_volume_qos(
                   context, instance)
        LOG.debug("query qos of instance: %s, qos_config: %s",
                  instance.id, qos_config)
        return {'qos_config': qos_config}

    #@wsgi.response(202)
    @wsgi.Controller.api_version("2.1")
    @wsgi.expected_errors(404)
    @validation.schema(server_volume_qos.qos_config)
    def set(self, req, server_id, body):
        """Permit admins to (live) migrate a server to a new host."""
        context = req.environ["nova.context"]
        #context.can(ms_policies.POLICY_ROOT % 'migrate_live')
        try:
            instance = common.get_instance(self.compute_api, context, server_id)
            LOG.debug("qos_config: %s", body)
            qos_result = self.compute_api.set_volume_qos(
                context, instance, body)
            return {'qos_config': qos_result}
        except exception.NotFound as e:
            msg = str(e)
            raise exc.HTTPNotFound(explanation=msg)

