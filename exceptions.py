class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidCommandLineUsageError(Error):
    """Raised when user does not supply a valid system in command line for Android Studio."""


class InvalidChoiceError(Error):
    """Raised when user does not choose a valid IDE, level, system or topic."""


class IncorrectAnswer(Error):
    """Raised when user gets an answer wrong"""
