"""Class of the messages printing."""
import csv
import os
import re
from datetime import datetime
from pathlib import Path

from pretty_verbose import LoggerErrorBase, MissingLogFolderError, RunningError
from pretty_verbose.constants import colors


class VerboseMessages:
    """
    The class that abstract a printer.

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
        Name of the scope to know who is printing the message.

    scope: Str. Default: "".
        Alias for name (Will be removed in future releases).

    filename: Path, Str. Default: "messages.log".
        Log file in which save the verbose output.

    sep: Str. Default: ";".
        Separator of the log file.

    overwrite: Bool. Default: False.
        Overwrite the log file.

    no_save: Bool. Default: False.
        When active prevents the output saving.

    """

    def __init__(
        self, level=1, name="", scope="", filename="messages.log", sep=";",
        overwrite=False, no_save=False
    ):
        """Construct the class."""
        # Set verbose level.
        self.level = level

        # Set verbose scope.
        if name:
            self.name = self.scope = name
        else:
            self.name = self.scope = scope

        # Set verbose output file.
        self.filename = Path(filename).resolve()

        # Set the separator of the log file.
        self.sep = sep

        # No save flag.
        self.no_save = no_save
        if not self.no_save:
            # Init the log DataFrame.
            self.start_log(overwrite)

    def start_log(self, overwrite):
        """
        Star the log file.

        If the file does note exists or if the overwrite is activated, open a
        file an write the header.

        Parameters
        ----------
        overwrite: Bool.
            Flag indicating whether overwrite or not the log file.

        """
        # Check if the directory exists.
        if not self.filename.parent.exists():
            no_save, self.no_save = self.no_save, True
            p_folder = self.filename.parent
            self.warning(
                f"The log dir '{p_folder}' does not exist!"
            )

            if self.confirm("Do you want to create it?"):
                self.filename.parent.mkdir(parents=True)
                self.no_save = no_save
            else:
                self.error(
                    f"Logger folder '{p_folder}' does not exist",
                    "exiting program...",
                    err_class=MissingLogFolderError
                )

        if not self.filename.exists() or overwrite:
            with open(
                self.filename, "w", newline="", encoding="utf-8"
            ) as file:
                log_messages = csv.writer(file, delimiter=self.sep)
                log_messages.writerow(
                    ["message_type", "n_datetime", "message"]
                )

    def __add_message(self, message_type, right_now, message):
        """
        Add a new row to the log.

        Parameters
        ----------
        message_type: Str.
            Typo off message, (DEBUG, ERROR, WARNING, INFO).

        right_now: Str.
            Time of the message.

        message: Str.
            Message text.

        """
        with open(self.filename, "a", newline="", encoding="utf-8") as file:
            log_messages = csv.writer(file, delimiter=self.sep)
            log_messages.writerow([message_type, right_now, message])

    def get_time(self):
        """
        Print the time in the color given.

        Parameters
        ----------
        color: Color.
            Color for the console text.

        Returns
        -------
            String with the actual time.

        """
        now = datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")
        return now

    def format_message(self, message_type, message, decorator=" "):
        """
        Print the message in the color given.

        Parameters
        ----------
        color: Color.
            Color for the console text.

        message_type: str.
            Type of message.

        message: Str.
            Message text.

        decorator: Str. Default: " ".
            Decorator to initialize the message.

        Returns
        -------
            String with the message in color.

        """
        text = (
            f"[{message_type}] [{self.scope}]:{decorator}" +
            f"{colors.RESET}{message}"
        )
        return text

    def get_terminal_columns(self):
        """
        Return the number of columns of the terminal.

        Returns
        -------
            Integer, number of columns of the terminal.

        """
        try:
            return os.get_terminal_size().columns
        except OSError:
            return 80

    def log(
        self, min_level, name, color, *message, decorator=" ", end="\n",
        skip_save=False
    ):
        """
        Print a log message with name, color and decorator.

        Parameters
        ----------
        min_lebel: Int.
            Minimum level of verbose to print the message.

        name: Str.
            Type of message.

        color: Color.
            Color for the console text.

        message: Str.
            Message text.

        decorator: Str. Default: " ".
            Decorator to initialize the message.

        end: Str. Default: "\n".
            End of the line for the printing.

        skip_save: Bool. Default: False.
            Skip saving the log to a file.

        """
        if self.level >= min_level:
            # Get time in the given color.
            now = self.get_time()

            # Join messages.
            message = ", ".join(f"{el}" for el in message)

            # Print message in the given color.
            print(
                (
                    color + now + self.format_message(name, message, decorator)
                ).ljust(self.get_terminal_columns()),
                end=end
            )

            if self.no_save or skip_save:
                return

            # Add message to log file.
            self.__add_message(name, now, f"{message}")

    def error(self, *message, err_id=0, err_str="", err_class=None, **opts):
        """
        Print an error message.

        Parameters
        ----------
        message: Str.
            Message text.

        err_id: Int | Str. Default: 0.
            If different of 0, "" or None, the function will print a message
            and will exit the process. This argument represents the id of the
            error.

        err_str: Str. Default: "".
            If different of "" or None, it will be printed as the error string
            identifier.

        err_class: Exception. Default: None.
            If an exception, it will be raised.

        **opts:
            Arguments passed to VerboseMessages.

        """
        if err_id:
            if isinstance(err_class, LoggerErrorBase):
                raise err_class(*message)
            if isinstance(err_class, RunningError):
                raise err_class(*message, err_id=err_id, err_str=err_str)

            if err_str:
                err_msg = f"[Error {err_id} ({err_str})]: "
            else:
                err_msg = f"[Error {err_id}]: "

            err_msg += ",".join(f"{el}" for el in message)

            if isinstance(err_class, Exception):
                raise err_class(colors.RED + err_msg)

            if not isinstance(err_id, int):
                err_id = 1

            self.log(0, "ERROR", colors.RED, err_msg, **opts)
            exit(err_id)

        else:
            self.log(0, "ERROR", colors.RED, *message, **opts)

    def warning(self, *message, **opts):
        """
        Print a warning message.

        Parameters
        ----------
        message: Str.
            Message text.

        **opts:
            Arguments passed to VerboseMessages.

        """
        self.log(1, "WARNING", colors.YELLOW, *message, **opts)

    def success(self, *message, **opts):
        """
        Print a success message.

        Parameters
        ----------
        message: Str.
            Message text.

        **opts:
            Arguments passed to VerboseMessages.

        """
        self.log(2, "SUCCESS", colors.GREEN, *message, **opts)

    def info(self, *message, **opts):
        """
        Print an info message.

        Parameters
        ----------
        message: Str.
            Message text.

        **opts:
            Arguments passed to VerboseMessages.

        """
        self.log(3, "INFO", colors.BLUE, *message, **opts)

    def for_message(self, *message, **opts):
        """
        Print a for loop message.

        Parameters
        ----------
        message: Str.
            Message text.

        **opts:
            Arguments passed to VerboseMessages.

        """
        deco = opts.pop("decorator", " - ")
        self.log(3, "INFO", colors.BLUE, *message, decorator=deco, **opts)

    def progress(self, message, percentage, **opts):
        """
        Print the progress percentage.

        Parameters
        ----------
        message: Str.
            Message text.

        percentage: Float.
            Percentage of progress of the process.

        **opts:
            Arguments passed to VerboseMessages.

        """
        end = opts.pop("end", None)
        if not end and float(f"{percentage:.2f}") < 100:
            end = "\r"
        elif not end:
            end = "\n"

        self.for_message(f"{message}: [{percentage:.2f}%]", end=end, **opts)

    def end_progress(self, process="process", **opts):
        """
        Print the end of the process.

        Parameters
        ----------
        process: Str.
            Process name text.

        **opts:
            Arguments passed to VerboseMessages.

        """
        deco = opts.pop("decorator", " - ")
        self.log(
            2, "SUCCESS", colors.GREEN, f"{process} done", decorator=deco,
            **opts
        )

    def debug(self, *message, **opts):
        """
        Print a debug message.

        Parameters
        ----------
        message: Str.
            Message text.

        **opts:
            Arguments passed to VerboseMessages.

        """
        self.log(4, "DEBUG", colors.MAGENTA, *message, **opts)

    def input(self, *message, input_text="INPUT", **opts):
        """
        Print an input message and return the response.

        Parameters
        ----------
        message: Str.
            Message text.

        input_text: Str.
            Text to be shown before the user input.

        **opts:
            Arguments passed to VerboseMessages.

        Returns
        -------
            String with the response.

        """
        self.log(-1e9, "INPUT", colors.CYAN, *message, **opts)

        try:
            # Print message in blue.
            response = input(colors.CYAN + f"{input_text} >> " + colors.RESET)

        except EOFError:
            self.warning("Exiting the program")
            exit(0)

        except KeyboardInterrupt:
            self.error("Action aborted by the user")
            exit(1)

        # Print time in magenta.
        now = self.get_time()

        # Add message to log file.
        self.__add_message("USER INPUT", now, f"{response}")

        return response

    def confirm(self, *message, **opts):
        """
        Print a confirmation message and return the response when it is valid.

        Parameters
        ----------
        message: Str.
            Message text.

        **opts:
            Arguments passed to VerboseMessages.

        Returns
        -------
            Bool with the confirmation value.

        """
        while True:
            # Print input message.
            response = self.input(*message, input_text="[Y/n]", **opts)

            if re.fullmatch(r"([Yy](es)?)?", response) is not None:
                return True

            elif re.match(r"[Nn]o?", response) is not None:
                return False

            else:
                self.warning("Unknown option.")
