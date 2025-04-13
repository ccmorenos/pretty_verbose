"""Classes of the Processes."""
import re
from datetime import datetime

from pretty_verbose.messages_classes import VerboseMessages


class Task(VerboseMessages):
    """Class that abstracts a task, which communicate its status.

    Parameters
    ----------
    level: Int.
        Level of verbose for the console output.
        -1: Nothing.
        0: just Errors.
        1: Errors and Warnings.
        2: Errors Warnings and Success.
        3: Errors Warnings, Success and Info.
        4: Errors Warnings, Success, Info and Debug.

    name: Str.
        Name of the scope to know which task prints the message.

    timer: Bool. Default: False.
        Initialize the timer or the task.

    process: Bool. Default: None.
        Parent process.

    **config:
        Parameters passed to `VerboseMessages`.

    """
    # Structure of the process name.
    NAME_REGEX = r"^(([^ \n]+\.)*([^ \n]+:))?([^ \n.:]*)$"

    def __init__(
        self, level, name, timer=False, process=None, **config
    ):
        # Create messager.
        super().__init__(
            level=level, name=name,
            filename=config.pop("log_file", f"{name}.log"), **config
        )

        # Timer of the task.
        self.timer = {"ti": None, "tf": None, "diff": None, "on": False}

        # Start timer.
        if timer:
            self.start_timer()

        # Configure tree. (Parent process)
        if isinstance(process, Process):

            if process.has_task(self):
                self.name = self.scope = (
                    f"{process.name}:{self.get_parents()[3]}"
                )
            else:
                process.add_task(self)

    def __del__(self):
        """Show timer if active."""
        if self.timer["on"]:
            self.task_done(True)

    def __get_milliseconds(self, interval):
        """Get the time of the interval in milliseconds.

        Parameters
        ----------
        interval: datetime.timedelta.
            Delta interval from which convert seconds in milliseconds.

        """
        return interval.total_seconds()*1000

    def exec_time(self, exec_f, *args, print_timer=False):
        """Execute a function and measure the time it takes to complete.

        Parameters
        ----------
        exec_f: Callable.
            Function from wich measure the time.

        args: Any.
            List of arguments of the function.

        print_timer: Bool. Default: Fasle.
            Whether print or not the timer value after stopping it.

        """
        self.start_timer()
        exec_f(*args)
        return self.task_done(print_timer)

    def exec_many_time(self, *exec_fs, args, print_timer=False, lap=False):
        """
        Execute a list of functions and measure the time it takes to complete.

        Parameters
        ----------
        exec_f: Callable.
            Function from wich measure the time.

        args: Array.
            List of arguments of each of the functions.

        lap: Bool. Default: Fasle.
            Whether print or not the timer value after each function.

        print_timer: Bool. Default: Fasle.
            Whether print or not the timer value after stopping it.

        """
        self.start_timer()
        for i, exec_f in exec_fs:
            exec_f(*args[i])
            if lap:
                self.print_lap()
        return self.task_done(print_timer)

    def get_parents(self):
        """Extract the parents from the name.

        Returns
        -------
            parents, gran_parents, parent, name: Strings with the parents
            processes, gan-parents (parents without counting the immediate
            parent process) processes, the immediate parent, the name of the
            task.

        """
        n_parts = re.match(self.NAME_REGEX, self.name)
        if n_parts is not None:
            return (
                "" if n_parts[1] is None else n_parts[1][:-1],
                "" if n_parts[2] is None else n_parts[2][:-1],
                "" if n_parts[3] is None else n_parts[3][:-1],
                "" if n_parts[4] is None else n_parts[4]
            )

        # Return void if the match fails.
        return "", "", "", self.name

    def reset_timer(self):
        """Reset the timer of the task."""
        self.timer = {"ti": None, "tf": None, "diff": None, "on": False}

    def start_timer(self):
        """Save the actual time and switch the timer on."""
        if self.timer["on"]:
            self.warning("Timer already running...")
            return

        self.timer["ti"] = datetime.now()
        self.timer["diff"] = None
        self.timer["on"] = True

    def lap(self):
        """Return the partial duration of the task."""
        if self.timer["on"]:
            lap_time = datetime.now() - self.timer["ti"]
            return self.__get_milliseconds(lap_time)

        self.warning("Timer is not running...")
        return None

    def stop_timer(self):
        """Stop the timer of the task."""
        if not self.timer["on"]:
            self.warning("Timer already stopped...")
            return

        self.timer["tf"] = datetime.now()
        self.timer["diff"] = self.timer["tf"] - self.timer["ti"]
        self.timer["on"] = False

    def total_time(self):
        """Return the time the task took.

        If the timer is still running, returning the lap.

        """
        if self.timer["on"]:
            self.warning("Timer is still running. Returning lap...")
            return self.lap()

        if self.timer["diff"] is None:
            self.warning("Timer have not been started...")
            return None

        return self.__get_milliseconds(self.timer['diff'])

    def task_done(self, print_timer=False):
        """Stop the timer of the task and print the total timer.

        Parameters
        ----------
        print_timer: Bool. Default: Fasle.
            Whether print or not the timer value after stopping it.

        """
        self.stop_timer()
        if print_timer:
            self.info(f"Task done in: {self.total_time()}ms")

        return self.total_time()

    def print_lap(self):
        """Stop the timer of the task and print the total timer."""
        self.info(f"Task lap: {self.lap()}ms")

    def get_depth(self):
        """Abstract method for the process methods."""
        return 0


class Process(Task):
    """Class that abstracts a process, which can add more tasks and processes.

    Parameters
    ----------
    level: Int.
        Level of verbose for the console output.
        -1: Nothing.
        0: just Errors.
        1: Errors and Warnings.
        2: Errors Warnings and Success.
        3: Errors Warnings, Success and Info.
        4: Errors Warnings, Success, Info and Debug.

    name: Str.
        Name of the scope to know which process prints the message.

    log_dir: Path, Str. Default: ".".
        Directory for the output log files.

    depth: Task. Default: None.
        Depth of the process.

    process: Task. Default: None.
        Parent process.

    **config:
        Parameters passed to `Task`.

    """
    __depth = 0

    NAME_REGEX = r"^(([^ \n]+\.)*([^ \n]+\.))?([^ \n.:]*)$"
    MAX_DEPTH = 5

    def __init__(
        self, level, name, log_dir=".", depth=None, process=None, **config
    ):
        # Create task.
        super().__init__(
            level, name, log_dir=log_dir,
            log_file=config.pop("log_file", f"{name}.log"), **config
        )

        self.subprocesses = {}
        self.tasks = {}

        # Configure tree. (Parent process)
        if isinstance(depth, Process):
            self.__config_depth(depth)

        elif isinstance(process, Process):
            self.__config_depth(process)

            if process.has_subprocess(self):
                self.name = self.scope = (
                    f"{process.name}.{self.get_parents()[3]}"
                )
            else:
                process.add_subprocess(self)

        else:
            self.__depth = 0

    def __config_depth(self, process):
        """
        Set the depth of the process.

        Parameters
        ----------
        process: Task.
            Parent process which determine the depth.

        """
        if process.get_depth() + 1 >= self.MAX_DEPTH:
            self.error(
                "Max recursivity depth reached, please reduce the "
                "recursivity depth or change the max depth parameter",
                err_id=104, err_str="MAX DEPTH REACHED"
            )

        self.__depth = process.get_depth() + 1

    def get_depth(self):
        """Return the depth of the process."""
        return self.__depth

    def new_task(self, name, **config):
        """Add a new task to the process.

        Parameters
        ----------
        name: Str.
            Name of the scope to know which task prints the message.

        **config:
            Parameters passed to `Task`.

        Returns
        -------
            The new task.

        """
        self.tasks[f"{self.name}:{name}"] = Task(
            self.level, f"{self.name}:{name}",
            log_dir=config.pop("log_dir", self.output_conf().log_dir),
            sep=config.pop("sep", self.output_conf().sep),
            overwrite=config.pop("overwrite", self.output_conf().overwrite),
            no_save=config.pop("no_save", self.output_conf().no_save),
            **config
        )

        return self.tasks[f"{self.name}:{name}"]

    def add_task(self, task):
        """Add a new task to the process.

        Parameters
        ----------
        task: Task.
            Task to be added.

        """
        _, _, _, name = task.get_parents()
        self.tasks[f"{self.name}:{name}"] = task

    def has_task(self, task):
        """Check if the task is in the process.

        Parameters
        ----------
        task: Task.
            Task to be checked.

        """
        parents, _, _, name = task.get_parents()

        if parents != "" and parents != self.name:
            self.error(
                f"Task belongs to another process: {parents}.",
                err_id=105, err_str="INCOMPATIBLE PARENTS"
            )

        return self.tasks.get(f"{self.name}:{name}", None) is not None

    def new_subprocess(self, name, **config):
        """Add a new subprocess to the process.

        Parameters
        ----------
        name: Str.
            Name of the scope to know which process prints the message.

        **config:
            Parameters passed to `Process`.

        Returns
        -------
            The new process.

        """
        self.subprocesses[f"{self.name}.{name}"] = Process(
            self.level, f"{self.name}.{name}",
            config.pop("log_dir", self.output_conf().log_dir),
            sep=config.pop("sep", self.output_conf().sep),
            overwrite=config.pop("overwrite", self.output_conf().overwrite),
            no_save=config.pop("no_save", self.output_conf().no_save),
            depth=self, **config
        )

        return self.subprocesses[f"{self.name}.{name}"]

    def add_subprocess(self, process):
        """Add a new subprocess to the process.

        Parameters
        ----------
        process: Process.
            Process to be added.

        """
        _, _, _, name = process.get_parents()
        self.tasks[f"{self.name}.{name}"] = process

    def has_subprocess(self, process):
        """Check if the subprocess is in the process.

        Parameters
        ----------
        process: Process.
            Process to be checked.

        """
        parents, _, _, name = process.get_parents()

        if parents not in ("", self.name):
            self.error(
                f"Processor belongs to another process: {parents}.",
                err_id=105, err_str="INCOMPATIBLE PARENTS"
            )

        return self.subprocesses.get(f"{self.name}.{name}", None) is not None
