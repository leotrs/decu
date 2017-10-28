import os
import configparser
from string import Template

__all__ = ['config']

config_filename = 'decu.cfg'


class DecuParser(configparser.ConfigParser):
    def subs(self, section, option, **kwargs):
        return Template(self.get(section, option)).safe_substitute(**kwargs)


class DecuSectionProxy(configparser.SectionProxy):
    def subs(self, option, **kwargs):
        return Template(self.get(option)).safe_substitute(**kwargs)


configparser.SectionProxy = DecuSectionProxy
config = DecuParser(interpolation=None)
config.read([os.path.join(os.path.dirname(__file__), config_filename),
             os.path.expanduser('~/.{}'.format(config_filename)),
             os.path.join(os.getcwd(), config_filename)])
