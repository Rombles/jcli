# The purpose of this file is to provide all the custom, descriptive exceptions to JCLI
class JCLIException(Exception):
    pass


# Ovirt Authentication Error
class AuthenticationError(JCLIException):
    pass


# Ovirt Authentication Error
class OvirtCommonError(JCLIException):
    pass


# Directory Mount Error
class DirectoryMountException(JCLIException):
    pass


class NicConfigurationError(JCLIException):
    pass


class DiskException(JCLIException):
    pass


class TimeOutException(JCLIException):
    pass


class VmStatusException(JCLIException):
    pass
