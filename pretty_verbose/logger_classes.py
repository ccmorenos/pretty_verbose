"""Classes of the logger."""
import readline

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
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, level, name="Main", log_dir=".", **config):
        # create process.
        super().__init__(level, name, log_dir, **config)

        self.__history_file = self.output_conf().log_dir / ".history"

        if self.__history_file.exists():
            readline.read_history_file(self.__history_file)

    def __del__(self):
        """Function called when the object is deleted."""
        readline.write_history_file(self.__history_file)
        return super().__del__()

    def input(self, *message, input_text="INPUT", **opts):
        """
        Print an input message and return the response.

        Parameters
        ----------
        message: Str.
            Message text.

        input_text: Str.
            Text to be shown before the user input.

        skip_save: Bool. Default: False.
            Skip saving the log to a file.

        **opts:
            Arguments passed to VerboseMessages.

        Returns
        -------
            String with the response.

        """
        response = super().input(*message, input_text=input_text, **opts)
        readline.write_history_file(self.__history_file)
        return response
