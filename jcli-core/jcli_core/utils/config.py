import os
import pkgutil

from ast import literal_eval
from ConfigParser import SafeConfigParser
from ConfigParser import MissingSectionHeaderError


def read_config(path=None, section=None):
    """Takes a path to a config file and parses it returning the given section

    Args:
        path  (str) - path to the configuration file
        section (str) - configuration section to return

    Returns:
        dict: representation of configuration section
    """
    parser = SafeConfigParser(allow_no_value=True)
    if not path:
        path = os.path.join(os.getenv("HOME"), '.jcli.conf')

    cfg = {}
    if os.path.exists(path):
        try:
            parser.read(path)
        except MissingSectionHeaderError:
            print "Configuration file invalid. Using defaults"
    else:
        return cfg

    def as_dict(config):
        """Take the configuration parser object and create a dict
        """
        configuration_dict = {}
        for section in config.sections():
            sub_cfg = {}
            for key, val in config.items(section):
                if val != '':
                    try:
                        sub_cfg[key] = literal_eval(val)
                    except (ValueError, SyntaxError):
                        sub_cfg[key] = val
                else:
                    pass
            configuration_dict[section] = sub_cfg
        return configuration_dict

    cfg = as_dict(parser)

    if section:
        return cfg.get(section, {})
    else:
        return cfg


def merge_dicts(default, override):
    """ Merge two dictionaries

    Values in user dict and merge over defaults dictionary

    Args:
        dict:   default - Dictionary of default values
        dict:   user    - Dictionary of user-supplied varlues

    Returns:
        dict:   Combined dictionary
    """
    # Copy of defaults dict to preserve original
    context = default.copy()
    for key, value in override.iteritems():
        try:
            if value is not None:
                context[key] = value
        except KeyError:
            pass
    return context


def get_package_data_path(package, resource):
    """ Helper to get data files from a package

        Used to pull data from a package file, useful for fetching default
        configs/data files stored with the python module.

        Package resource must be relative to the top of the package directory

    Args:
        package (str): Package name to get data from.
        resource (str): Name of the file to get.

    Returns:
        str: Absolute path to the resource requested.

    Raises:
        IOError: If resource does not exist.
    """
    package = package.split('.')[0]
    loader = pkgutil.get_loader(package)
    parts = [package, os.path.dirname(loader.filename), package]
    parts.extend(resource.split('/'))
    resource_path = os.path.join(*parts)
    if not os.path.exists(resource_path):
        raise IOError("No such file or directory: '{0}'".format(resource_path))
    return resource_path
