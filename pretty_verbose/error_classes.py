"""Classes for the errors."""
from pretty_verbose.constants import colors, error_codes


class RunningError(Exception):
    """
    Class for a error of the running process.

    With this base class it is supposed to handle user customized errors.

    """

    def __init__(self, *message, err_id, err_str="", color=colors.RED):
        super().__init__(color + ",".join(f"{el}" for el in message))
        self.err_id = err_id
        self.err_str = err_str

    def __str__(self):
        """Return string with format."""
        help_str = "" if self.err_str else f" ({self.err_str})"
        return f"[Error {self.err_id}{help_str}]"


class LoggerErrorBase(RunningError):
    """Class for a error of the logger."""

    def __init__(self, *message, err_id=100):
        super().__init__(
            *message, err_id=err_id,
            err_str=error_codes.LOGGER_ERROR_CODES[err_id]
        )

    def __str__(self):
        """Return string with format."""
        help_str = "" if self.err_str else f" ({self.err_str})"
        return f"[Error L{self.err_id}{help_str}]"


class LoggerError(LoggerErrorBase):
    """Class for a error of the logger."""

    def __init__(self, *message):
        super().__init__(*message, err_id=100)


class MissingLogFolderError(LoggerErrorBase):
    """Class for a error of the logger."""

    def __init__(self, *message):
        super().__init__(*message, err_id=101)
