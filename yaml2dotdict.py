# -*- coding: utf-8 -*-
"""
A dict can read YAML data as its property. so you can easily access
the data by dot notion.

config = YAMLDict()
"""
import yaml

class YAMLDict(dict):
    """An YAML data can use dot notion access attributes
    
    """
    def __init__(self, args=None):
        if not args:
            return
        super(YAMLDict, self).__init__(args)
        if isinstance(args, dict):
            for k, v in args.iteritems():
                if not isinstance(v, dict):
                    self[k] = v
                else:
                    self.__setattr__(k, YAMLDict(v))


    def load(self,args):
        self.__init__(yaml.load(args))
        
    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(YAMLDict, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(YAMLDict, self).__delitem__(key)
        del self.__dict__[key]