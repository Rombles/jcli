"""
Set up a logger for the service being provided by jcli
"""
import logging
import os

from logging.handlers import RotatingFileHandler


class JLogger(object):
    """ Logger """
    def __init__(self, name=None, level=0):
        """ Set up logger for jcli
        Args:
            str:    logfile - path to logfile
            int:    level - logging level
                        0 - ERROR
                        1 - WARNING
                        2 - INFO
                        3 - DEBUG
        """
        self.logger = logging.getLogger(name)

        # Set up default verbosity
        verbosity_levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
        if level > len(verbosity_levels) - 1:
            level = len(verbosity_levels) - 1
        self.logger.setLevel(verbosity_levels[level])

        # File handler for .jcli.log file logs everything
        filehandler = RotatingFileHandler(
            os.path.join(os.environ.get('HOME'), '.jcli.log'),
            mode='a',
            maxBytes=5*1024*1024,
            backupCount=1
        )
        filehandler.setLevel(logging.DEBUG)

        # Stream Handler for Console
        consolehandler = logging.StreamHandler()

        # Formatting
        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
                                      datefmt="[%Y-%m-%d %H:%M:%S]")
        filehandler.setFormatter(formatter)
        consolehandler.setFormatter(formatter)

        # Add loggers to base logger
        self.logger.addHandler(filehandler)
        self.logger.addHandler(consolehandler)

    def msg(self, message, level='info'):
        """ Wrapper around logging functionality
        Args:
            str:    message - message to communicate
            str:    level - severity of message
                Levels:
                    debug (10), info (20), warning (30), error (40), critical (50)
        """
        getattr(self.logger, level)(message)
