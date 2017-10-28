"""
config.py
---------

Custom configuration parsing for decu, based on configparser.

"""
import os
import configparser
from string import Template

__all__ = ['config', 'DecuParser']

config_filename = 'decu.cfg'


class DecuParser(configparser.ConfigParser):
    """ConfigParser subclass for decu.

    Treat every option in the config file as a string.Template object.

    """
    def subs(self, section, option, **kwargs):
        """Perform the named substitutions on the option.

        Each option in the decu configuration file is treated as a
        string.Template object, and thus accepts named variables for
        substitution. To read a raw option from the configuration file, do
        decu.config[section][option]. To read a substituted option, do
        decu.config.subs(section, option, kwargs) or
        decu.config.subs[section].subs(option, kwargs), where every
        keyword argument is a name=string pair to be substituted in the
        option.

        Args:
            section (str): the desired section.
            option (str): the desired option.
            kwargs (dict): every keyword argument is a name=string pair to
                be substituted in the option template.

        Returns:
            str: the option template with the named strings substituted in.

        """
        return Template(self.get(section, option)).safe_substitute(**kwargs)


class DecuSectionProxy(configparser.SectionProxy):
    """SectionProxy subclass for decu.

    Treat every option in the config file as a string.Template object.

    """
    def subs(self, option, **kwargs):
        """Perform the named substitutions on the option.

        See also:
            DecuParser.subs.

        """
        return Template(self.get(option)).safe_substitute(**kwargs)


configparser.SectionProxy = DecuSectionProxy
config = DecuParser(interpolation=None)
config.read([os.path.join(os.path.dirname(__file__), config_filename),
             os.path.expanduser('~/.{}'.format(config_filename)),
             os.path.join(os.getcwd(), config_filename)])
