"""Classes of the logger."""
from pathlib import Path

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
        Parameters passed through `Process`.

    """

    def __init__(
        self, level, name="Main",
        log_dir=Path("."), log_file="logger.log", **config
    ):
        # Resolve the output directory.
        self.log_dir = Path(log_dir).resolve()

        # No save flag.
        no_save = config.pop("no_save", False)

        # create process.
        super().__init__(
            level, name, log_file=self.log_dir/log_file, no_save=True, **config
        )

        # Check if the directory exists.
        if not self.log_dir.exists():
            self.warning(f"The log dir '{self.log_dir}' does not exist!")

            if self.confirm("Do you want to create it?"):
                self.log_dir.mkdir()
            else:
                self.error(
                    "Logger folder does not exist, exiting...",
                    err_id=101, err_msg="MISSING FOLDER"
                )

        # Update no save.
        self.no_save = no_save
        if not self.no_save:
            self.start_log(config.pop("overwrite", False))

    def new_task(self, name, log_file, **config):
        """Add a new task to the process.

        Parameters
        ----------
        name: Str.
            Name of the scope to know which task prints the message.

        log_file: Path, Str.
            Log file in which save the verbose output.

        **config:
            Parameters passed through `Task`.

        Returns
        -------
            The new task.

        """
        return super().new_task(name, self.log_dir/log_file, **config)

    def new_subprocess(self, name, log_file, **config):
        """Add a new subprocess to the process.

        Parameters
        ----------
        name: Str.
            Name of the scope to know which process prints the message.

        log_file: Path, Str.
            Log file in which save the verbose output.

        **config:
            Parameters passed through `Process`.

        Returns
        -------
            The new process.

        """
        return super().new_subprocess(name, self.log_dir/log_file, **config)
