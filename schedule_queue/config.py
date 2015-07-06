# For making Tools for scheduling app

import sys
import inspect

# Function calls for pseudo-model


def get_tool_choices():
    tool_choices = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            tool_choices.append((obj.get_slug(), obj.get_name()))
    return tuple(tool_choices)


def get_tool_list():
    tool_list = [x for x in tool]
    return tool_list


def get_tool_info(slug):
    return tool[slug]


# Tool definitions

class D180(object):

    @staticmethod
    def get_name():
        return 'D180'

    @staticmethod
    def get_slug():
        return 'd180'


class D75(object):

    @staticmethod
    def get_name():
        return 'D75'

    @staticmethod
    def get_slug():
        return 'd75'

# custom attributes for tools
tool = {
    'd180': {
        'slug': D180.get_slug(),
        'max_reservations': 8,
        'process_start_url': 'create_growth_d180_start',
    },
    'd75': {
        'slug': D75.get_slug(),
        'max_reservations': 8,
    },
}
