from os import error


class Error:
    name = None
    description = None
    show_full_description = False

class ModuleDoesNotExist(Error):
    pass

class NotLinePass(Error):
    pass

class MBSyntaxError(Error):
    pass

class UnDefineError(Error):
    pass

class ConditionError(Error):
    pass

class ModuleImportError(Error):
    pass

class UnknownCommand(Error):
    pass