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

from nova.api.validation import parameter_types

qemu_agent_command = {
    'type': 'object',
    'properties': {
        'qemuAgentCommand': {
            'type': 'object',
            'properties': {
                'execute': parameter_types.qemu_agent_command_execute,
                'arguments': parameter_types.qemu_agent_command_arguments,
            },
            'required': ['execute'],
            'additionalProperties': False,
        },
    },
    'required': ['qemuAgentCommand'],
    'additionalProperties': False,
}
