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

from nova.api.openstack import common
from nova.api.openstack import wsgi
# from nova import compute
from nova.compute import api
from nova import exception
from nova.i18n import _

ALIAS = "os-qemu-agent-command"


class QemuAgentCommandController(wsgi.Controller):

    def __init__(self, *args, **kwargs):
        super(QemuAgentCommandController, self).__init__(*args, **kwargs)
        self.compute_api = api.API()

    @wsgi.action('qemuAgentCommand')
    @wsgi.response(200)
    def qemu_agent_command(self, req, id, body):
        context = req.environ['nova.context']

        execute = body['qemuAgentCommand']['execute']
        arguments = body['qemuAgentCommand']['arguments']
        instance = common.get_instance(self.compute_api, context, id)
        try:
            return self.compute_api.qemu_agent_command(
                context, instance, execute, arguments)
        except exception.InstanceNotReady as e:
            raise exc.HTTPNotFound(explanation=e.format_message())
        except exception.InstanceQemuAgentCommandFailed as e:
            raise exc.HTTPConflict(explanation=e.format_message())
        except exception.InstanceInvalidState as e:
            raise common.raise_http_conflict_for_instance_invalid_state(
                e, 'qemuAgentCommand', id)
        except NotImplementedError:
            msg = _("Unable to execute qemu agent command on instance")
            common.raise_feature_not_supported(msg=msg)
