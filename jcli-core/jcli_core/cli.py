"""Usage:
   jcli [-v... ] [-o FILEPATH] [--cfg=FILE] <command> [<args> ...]
   jcli [-h]
   jcli [--version]

Options:
   -h, --help               Show this help message
   --cfg CONFIG             User given config file
   --verision               Show tool version
   -v                       Increase verbosity
   -o, --output FILEPATH    Output filepath

See jcli <command> help for more information
"""
import os

from . import __version__ as VERSION
from docopt import docopt
from prettytable import PrettyTable

from jcli_core.jlogger import JLogger
from jcli_core.iplugin import discover_plugins_pkgresources
from jcli_core.iplugin import list_available_plugins

PACKAGE_PLUGIN_DIRECTORY = os.path.join(os.path.dirname(__file__), 'plugins')


def main():
    # Initial Parser, disable help to show custom help message
    doc_args = docopt(__doc__, version=VERSION or 'dev', help=False, options_first=True)

    # Set up logging
    verbosity = doc_args.get('-v')
    JLogger(name=__package__, level=verbosity)

    # TODO: Add user config plugin directory to plugin_dir
    command = doc_args.pop('<command>')
    registered_plugins = discover_plugins_pkgresources()

    try:
        registered_plugins.get(command)(options=doc_args).run_hook()
    except TypeError:
        print __doc__
        print "Available Plugins:"
        table = PrettyTable(['Plugin', 'Description'])
        table.align = 'l'  # Left align all columns
        for plugin in list_available_plugins():
            name, operator = plugin
            table.add_row([name, operator.__description__])
        print table
        print "\nFor additional help, type: jcli <plugin> --help"


if __name__ == '__main__':
    main()
