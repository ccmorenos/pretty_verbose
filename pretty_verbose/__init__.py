"""This file manage all the verbose prints."""
from datetime import datetime

import pandas as pd
from colorama import Fore, Style


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

    """

    def __init__(self, level=2, scope="", filename="messages.log"):
        """Construct the class."""
        # Set verbose level.
        self.level = level

        # Set verbose scope.
        self.scope = scope

        # Set verbose output file.
        self.filename = filename

        # Init the log DataFrame.
        self.log_messages = None
        self.start_log()

    def start_log(self):
        """
        Star the log file.

        Try to read the log file, create an empty DataFrame if the file do not
        exists or and error occurs.

        """
        try:
            self.log_messages = pd.read_csv(
                self.filename, sep=" ", index_col=0
            )
        except Exception:
            self.log_messages = pd.DataFrame({
                "type": [],
                "n_datetime": [],
                "message": []
            })

    def add_message(self, type, rightnow, message):
        """
        Add a new row to the log.

        Parameters
        ----------
        type: Str.
            Typo off message, (DEBUG, ERROR, WARNING, INFO).

        rightnow: Str.
            Time of the message.

        message: Str.
            Message text.

        """
        # Create new row schema.
        row_schema = {
            "type": [type],
            "n_datetime": [rightnow],
            "message": [message]
        }

        # Append row.
        self.log_messages = pd.concat(
            [self.log_messages, pd.DataFrame(row_schema)], ignore_index=True
        )

        # Save log file.
        self.save_log()

    def save_log(self):
        """Save the log in the given file."""
        self.log_messages.to_csv(self.filename, index=False, sep=" ")

    def print_time(self, color):
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
        print(color + now, end=" ")
        return now

    def debug(self, *message):
        """
        Print a debug message.

        Parameters
        ----------
        message: Str.
            Message text.

        """
        if self.level >= -1:
            # Print time in magenta.
            now = self.print_time(Fore.MAGENTA)

            # Join messages.
            message = ", ".join(f"{el}" for el in message)

            # Print message in magenta.
            print(
                Fore.MAGENTA + f"DEBUG [{self.scope}]: " +
                Style.RESET_ALL + f"{message}"
            )

            # Add message to log file.
            self.add_message("DEBUG", now, f"{message}")

    def error(self, *message):
        """
        Print an error message.

        Parameters
        ----------
        message: Str.
            Message text.

        """
        if self.level >= 0:
            # Print time in red.
            now = self.print_time(Fore.RED)

            # Join messages.
            message = ", ".join(f"{el}" for el in message)

            # Print message in red.
            print(
                Fore.RED + f"ERROR [{self.scope}]: " +
                Style.RESET_ALL + f"{message}"
            )

            # Add message to log file.
            self.add_message("ERROR", now, f"{message}")

    def warning(self, *message):
        """
        Print a warning message.

        Parameters
        ----------
        message: Str.
            Message text.

        """
        if self.level >= 1:
            # Print time in yellow.
            now = self.print_time(Fore.YELLOW)

            # Join messages.
            message = ", ".join(f"{el}" for el in message)

            # Print message in yellow.
            print(
                Fore.YELLOW + f"WARNING [{self.scope}]: " +
                Style.RESET_ALL + f"{message}"
            )

            # Add message to log file.
            self.add_message("WARNING", now, f"{message}")

    def success(self, *message):
        """
        Print a warning message.

        Parameters
        ----------
        message: Str.
            Message text.

        """
        if self.level >= 2:
            # Print time in green.
            now = self.print_time(Fore.GREEN)

            # Join messages.
            message = ", ".join(f"{el}" for el in message)

            # Print message in green.
            print(
                Fore.GREEN + f"SUCCESS [{self.scope}]: " +
                Style.RESET_ALL + f"{message}"
            )

            # Add message to log file.
            self.add_message("SUCCESS", now, f"{message}")

    def info(self, *message):
        """
        Print an info message.

        Parameters
        ----------
        message: Str.
            Message text.

        """
        if self.level >= 3:
            # Print time in blue.
            now = self.print_time(Fore.BLUE)

            # Join messages.
            message = ", ".join(f"{el}" for el in message)

            # Print message in blue.
            print(
                Fore.BLUE + f"INFO [{self.scope}]: " +
                Style.RESET_ALL + f"{message}"
            )

            # Add message to log file.
            self.add_message("INFO", now, f"{message}")

    def for_message(self, message):
        """
        Print a for loop message.

        Parameters
        ----------
        message: Str.
            Message text.

        """
        if self.level >= 3:
            # Print time in blue.
            now = self.print_time(Fore.BLUE)

            # Print message in blue.
            print(
                Fore.BLUE + f"INFO [{self.scope}] -- " +
                Style.RESET_ALL + f"{message}"
            )

            # Add message to log file.
            self.add_message("INFO", now, f"{message}")

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
        if self.level >= 3:
            # Print time in blue.
            now = self.print_time(Fore.BLUE)

            # Print process status in blue.
            print(
                Fore.BLUE + f"INFO [{self.scope}] -- " +
                Style.RESET_ALL + f"{message}: [{percentage:.2f}%]", end="\r"
            )

            # Add message to log file.
            self.add_message(
                "INFO", now, f"{message}: [{percentage:.2f}%]"
            )

    def end_progress(self, process="process"):
        """
        Print the end of the process.

        Parameters
        ----------
        process: Str.
            Process name text.

        """
        if self.level >= 3:
            # Print time in blue.
            now = self.print_time(Fore.BLUE)

            # Print process status in blue.
            print(
                Fore.BLUE + f"INFO \t[{self.scope}] -- " +
                Style.RESET_ALL + f"{process} done"
            )

            # Add message to log file.
            self.add_message("INFO", now, f"{process} done")
