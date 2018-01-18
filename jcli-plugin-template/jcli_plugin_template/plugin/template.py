#! /usr/bin/env python
import logging
import sys

from jcli_core.iplugin import IPlugin
from jcli_core.iplugin import SubCommand
from jcli_core.utils import config

# Set up default config (Merge of package config and user config)
PACKAGE_CONFIG = config.read_config(
    path=config.get_package_data_path(__package__, 'conf/template.conf'),
    section='template'
)
USER_CONFIG = config.read_config(section='template')
MERGE_CONFIG = config.merge_dicts(PACKAGE_CONFIG, USER_CONFIG)


class Example(IPlugin):
    """Usage:
    example [-n NAME ...] <command> [<args> ...]
    example [-h]

Options:
    -n, --name NAME     example(s) to operate on
    -h, --help          Show this help message
    """
    __description__ = 'Manage examples managed by jcli'

    def __init__(self, *pargs, **kwargs):
        super(self.__class__, self).__init__(*pargs, **kwargs)
        self.logger = logging.getLogger(IPlugin.__module__)

    def run_hook(self):
        # Extract run options
        self.logger.debug('Example.run() invoked')
        return self._run_hook()

    def _run_hook(self):
        self.logger.info("Running hook: {0}".format(__name__))
        self.logger.debug("Available commands: {0}".format(
            [cmd.__name__.lower() for cmd in self.subcommands])
        )
        self.logger.debug("Command given: {0}".format(self.options.get('<command>')))
        self.logger.debug("Options parsed by docopt: {0}".format(self.options))
        for command in self.subcommands:
            if command.__name__.lower() == self.options.get('<command>'):
                commander = command(self.options, help_text=MERGE_CONFIG['--show-help'])

        try:
            commander.run()
        except NameError:
            if self.options.get('<command>'):
                print "Command not found: {0}".format(self.options.get('<command>'))
            print self.__doc__
            self._print_commands()


class ExampleCommand(SubCommand):
    """Usage:
    examplecommand [--option-a OPTIONA] [--option-b OPTIONB]

Options:
    --option-a OPTION	OPTION A TEST
    --option-b OPTION	OPTION B TEST
    -h, --help                  Show this help message
    """
    __description__ = 'ExampleCommand Description'

    def __init__(self, *pargs, **kwargs):
        """ Example Commands
        """
        super(self.__class__, self).__init__(*pargs, **kwargs)
        self.options = config.merge_dicts(MERGE_CONFIG, self.options)

    def run(self):
        self.logger.info("examplecommand invoked")
        self.logger.debug("examplecommand arguments parsed: {0}".format(self.options))
	print("You ran ExampleCommand!")
