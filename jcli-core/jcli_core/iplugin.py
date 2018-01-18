# -------------------------------------------------------------------------------
# jcli: jcli/iplugin.py
#
# The plugin interface. Plugins that want to register with jcli must inherit
# IPlugin.
#
# This code was borrowed heavily from:
#   https://github.com/eliben/code-for-blog/tree/master/2012/plugins_python
# -------------------------------------------------------------------------------
import inspect
import logging
import pkg_resources
import sys

from docopt import docopt
from prettytable import PrettyTable

from jcli_core.utils.config import merge_dicts


class IPlugin(object):
    __description__ = "IMPLEMENT DESCRIPTION"

    def __init__(self, options=None):
        """ Initialize the plugin.
        """
        opts = docopt(self.__doc__, help=False, options_first=True,
                      argv=options.pop('<args>'))
        self.options = merge_dicts(options, opts)
        self.subcommands = get_subcommands(sys.modules.get(self.__module__))

    def _print_commands(self):
        print "Available Commands:"
        table = PrettyTable(['Command', 'Description'])
        table.align = 'l'  # Left align all columns
        for subcommand in self.subcommands:
            table.add_row([subcommand.__name__.lower(), subcommand.__description__])
        print table

    def run_hook(self):
        raise NotImplemented("Implement a run hook!")


class SubCommand(object):
    __description__ = "UNIMPLEMENTED DESCRIPTION"

    def __init__(self, options=None, help_text=False):
        self.logger = logging.getLogger(IPlugin.__module__)
        opts = docopt(self.__doc__, help=help_text, options_first=True,
                      argv=options.pop('<args>'))
        self.options = merge_dicts(options, opts)

    def run(self):
        raise NotImplemented("Subcommands must implement a run method")


def get_subcommands(module):
    """ Get proper subclasses from given module
    """
    subclasses = []
    for cla in inspect.getmembers(module, inspect.isclass):
        if cla[0] != "SubCommand" and issubclass(cla[1], SubCommand):
            subclasses.append(cla[1])
    return subclasses


def discover_plugins_pkgresources():
    plugins = {}
    for entry_point in pkg_resources.iter_entry_points('jcli.plugins'):
        plugins[entry_point.name] = entry_point.load()

    return plugins


def list_available_plugins():
    plugins = []
    for directive, operator in discover_plugins_pkgresources().iteritems():
        plugins.append((directive, operator))
    return plugins
