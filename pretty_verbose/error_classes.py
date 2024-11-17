"""Classes for the errors."""


class LoggerError(Exception):
    """Class for a error of the logger."""

    def __init__(self, color, *message, err_id, err_str=""):
        super().__init__(color + ",".join(f"{el}" for el in message))
        self.err_id = err_id
        self.err_str = err_str

    def __str__(self):
        """Return string with format."""
        help_str = "" if self.err_str else f" ({self.err_str})"
        return f"[Error {self.err_id}{help_str}]"
