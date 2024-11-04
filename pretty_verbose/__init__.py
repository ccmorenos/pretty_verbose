"""This file manage all the verbose prints."""
import csv
import re
from datetime import datetime
from pathlib import Path


class VerboseMessages:
    """
    The class of the verbose prints.

    Parameters
    ----------
    level: Int.
        Level of verbose for the console output.
        -1: Just Debug.
        0: Debug and Errors.
        1: Debug, Errors and Warnings.
        2: Debug, Errors Warnings and Success.
        3: Debug, Errors Warnings, Success and Info.

    scope: Str.
        Name of the scope to know which process prints the message.

    filename: Path, Str.
        Log file in which save the verbose output.

    sep: Str.
        Separator of the log file.

    overwrite: Bool.
        Overwrite the log file.

    """
    # Color.
    MAGENTA = "\033[38;2;255;0;255m"
    RED = "\033[38;2;255;0;0m"
    YELLOW = "\033[38;2;255;255;0m"
    GREEN = "\033[38;2;50;200;50m"
    BLUE = "\033[38;2;50;150;255m"
    CYAN = "\033[38;2;0;255;255m"
    RESET = "\033[0m"

    def __init__(
        self, level=2, scope="", filename="messages.log", sep=";",
        overwrite=False
    ):
        """Construct the class."""
        # Set verbose level.
        self.level = level

        # Set verbose scope.
        self.scope = scope

        # Set verbose output file.
        self.filename = Path(filename).resolve()

        # Set the separator of the log file.
        self.sep = sep

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
        if not self.filename.exists() or overwrite:
            with open(self.filename, "w", newline="") as file:
                log_messages = csv.writer(file, delimiter=self.sep)
                log_messages.writerow(
                    ["message_type", "n_datetime", "message"]
                )

    def add_message(self, message_type, right_now, message):
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
        with open(self.filename, "a", newline="") as file:
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

    def format_message(self, color, message_type, message, decorator=" "):
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

        decorator: Str.
            Decorator to initialize the message.

        Returns
        -------
            String with the message in color.

        """
        text = (
            color + f"[{message_type}] [{self.scope}]:{decorator}" +
            self.RESET + f"{message}"
        )
        return text

    def log(
        self,
        min_level,
        name,
        color="\033[0m",
        *message,
        decorator=" ",
        end="\n"
    ):
        """
        Print a log message with name, color and decorator.

        Parameters
        ----------
        min_lebel: int.
            Minimum level of verbose to print the message.

        name: str.
            Type of message.

        color: Color.
            Color for the console text.

        message: Str.
            Message text.

        decorator: Str.
            Decorator to initialize the message.

        end: Str.
            End of the line for the printing.

        """
        if self.level >= min_level:
            # Get time in the given color.
            now = self.get_time()

            # Join messages.
            message = ", ".join(f"{el}" for el in message)

            # Print message in the given color.
            print(
                now +
                self.format_message(color, name, message, decorator),
                end=end
            )

            # Add message to log file.
            self.add_message(name, now, f"{message}")

    def debug(self, *message):
        """
        Print a debug message.

        Parameters
        ----------
        message: Str.
            Message text.

        """
        self.log(-1, "DEBUG", self.MAGENTA, *message)

    def error(self, *message):
        """
        Print an error message.

        Parameters
        ----------
        message: Str.
            Message text.

        """
        self.log(0, "ERROR", self.RED, *message)

    def warning(self, *message):
        """
        Print a warning message.

        Parameters
        ----------
        message: Str.
            Message text.

        """
        self.log(1, "WARNING", self.YELLOW, *message)

    def success(self, *message):
        """
        Print a success message.

        Parameters
        ----------
        message: Str.
            Message text.

        """
        self.log(2, "SUCCESS", self.GREEN, *message)

    def info(self, *message):
        """
        Print an info message.

        Parameters
        ----------
        message: Str.
            Message text.

        """
        self.log(3, "INFO", self.BLUE, *message)

    def for_message(self, *message):
        """
        Print a for loop message.

        Parameters
        ----------
        message: Str.
            Message text.

        """
        self.log(3, "INFO", self.BLUE, *message, decorator="--")

    def progress(self, message, percentage):
        """
        Print the progress percentage.

        Parameters
        ----------
        message: Str.
            Message text.

        percentage: Float.
            Percentage of progress of the process.

        """
        if float(f"{percentage:.2f}") < 100:
            end = "\r"
        else:
            end = "\n"

        self.log(
            3,
            "INFO",
            self.BLUE,
            f"{message}: [{percentage:.2f}%]",
            decorator="--",
            end=end
        )

    def end_progress(self, process="process"):
        """
        Print the end of the process.

        Parameters
        ----------
        process: Str.
            Process name text.

        """
        self.log(2, "SUCCESS", self.GREEN, f"{process} done", decorator="--")

    def input(self, *message, input_text="INPUT"):
        """
        Print an input message and return the response.

        Parameters
        ----------
        message: Str.
            Message text.

        input_text: Str.
            Text to be shown before the user input.

        Returns
        -------
            String with the response.

        """
        self.log(-10000, "INPUT", self.CYAN, *message)

        # Print message in blue.
        response = input(self.CYAN + f"{input_text} >> " + self.RESET)

        # Print time in magenta.
        now = self.get_time()

        # Add message to log file.
        self.add_message("USER INPUT", now, f"{response}")

        return response

    def confirm(self, *message):
        """
        Print a confirmation message and return the response when it is valid.

        Parameters
        ----------
        message: Str.
            Message text.

        Returns
        -------
            Bool with the confirmation value.

        """
        while True:
            # Print input message.
            response = self.input(*message, input_text="[Y/n]")

            if re.fullmatch(r"([Yy](es)?)?", response) is not None:
                return True

            elif re.match(r"[Nn]o?", response) is not None:
                return False

            else:
                self.warning("Unknown option.")
