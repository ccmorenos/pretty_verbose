"""Classes of the logger."""
from pretty_verbose.processes_classes import Process


class Logger(Process):
    """
    Class that abstracts a logger, with printers and processes.

    A logger is a module that administrates the terminal outputs of different
    proceses, and is able as well to create or delete processes.

    Parameters
    ----------
    level: Int. Default: 1.
        Level of verbose for the console output.
        -1: Nothing.
        0: just Errors.
        1: Errors and Warnings.
        2: Errors Warnings and Success.
        3: Errors Warnings, Success and Info.
        4: Errors Warnings, Success, Info and Debug.

    name: Str. Default: "".
        Name of the scope to know which logger is printing the message.

    log_dir: Path, Str. Default: ".".
        Directory for the output log files.

    log_file: Path, Str. Default: ".".
        Log file in which save the verbose output.

    **config:
        Parameters passed to `Process`.

    """

    def __init__(self, level, name="Main", log_dir=".", **config):
        # create process.
        super().__init__(level, name, log_dir, **config)
