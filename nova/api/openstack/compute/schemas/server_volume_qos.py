from nova.api.validation import parameter_types
from nova.api.validation.parameter_types import multi_params
from nova.objects import instance


qos_config = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'volume_id': parameter_types.volume_id,
            'device_name': {
                'type': 'string', 'minLength': 1, 'maxLength': 255,
                'pattern': '^[a-zA-Z0-9._-r/]*$',
             },
            'qos_specs': parameter_types.qos_specs,
         },
        'additionalProperties': False,
    }
}

