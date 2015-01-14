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
    tool_list = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            tool_list.append(obj.get_slug())
    return tuple(tool_list)

# custom attributes for tools
tool = {'d180': {'max_reservations': 5}, 'd75': {'max_reservations': 3}}

def get_tool_info(slug):
    return tool[slug]['max_reservations']

# Tool definitions

class d180(object):

    @staticmethod
    def get_name():
        return 'D180'

    @staticmethod
    def get_slug():
        return 'd180'

class d75(object):

    @staticmethod
    def get_name():
        return 'D75'

    @staticmethod
    def get_slug():
        return 'd75'
