# For making Tools for scheduling app

import sys
import inspect




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
            #return obj.get_slug()
            tool_list.append(obj.get_slug())
    return tuple(tool_list)

tool = {'d180': {'max_reservations': 5}, 'd75': {'max_reservations': 3}}

#def add_attributes():
#    for name, obj in inspect.getmembers(sys.modules[__name__]):
#        if inspect.isclass(obj):
#            obj.add_to_dict()  

def get_tool_info(slug):
    return tool[slug]['max_reservations']

#for name, obj in inspect.getmembers(sys.modules[__name__]):
#    if inspect.isclass(obj):
#        tool[obj.get_slug()]['tool_name'] = obj.get_name()

class d180(object):
    
    @staticmethod
    def get_name():
        return 'D180'
    
    @staticmethod
    def get_slug():
        return 'd180'
    
    #def add_to_dict():
    #    a = d180.get_slug()
    #    if not tool[a]['tool_name']:
    #        tool[a]['tool_name'] = d180.get_name()

class d75(object):
    
    @staticmethod
    def get_name():
        return 'D75'
    
    @staticmethod
    def get_slug():
        return 'd75'
    
    #def add_to_dict():
    #    a = d75.get_slug()
    #    if not tool[a]['tool_name']:
    #        tool[a]['tool_name'] = d75.get_name()


