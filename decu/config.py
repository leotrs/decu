import os
import configparser
from string import Template

__all__ = ['config']


class DecuParser(configparser.ConfigParser):
    def subs(self, section, option, **kwargs):
        return Template(self.get(section, option)).safe_substitute(**kwargs)


class DecuSectionProxy(configparser.SectionProxy):
    def subs(self, option, **kwargs):
        return Template(self.get(option)).safe_substitute(**kwargs)


configparser.SectionProxy = DecuSectionProxy
config = DecuParser(interpolation=None)
config.read([os.path.join(os.path.dirname(__file__), 'decu.cfg'),
             os.path.expanduser('~/.decu.cfg'),
             os.path.join(os.getcwd(), 'decu.cfg')])
