# Pretty Verbose
[![PyPI version](https://img.shields.io/pypi/v/pretty-verbose.svg)](https://pypi.org/project/pretty-verbose/)
[![License](https://img.shields.io/github/license/ccmorenos/pretty_verbose
)](https://github.com/ccmorenos/pretty_verbose/blob/main/LICENSE)
[![Test Python Package](https://github.com/ccmorenos/pretty_verbose/actions/workflows/test-python.yml/badge.svg?branch=main)](https://github.com/ccmorenos/pretty_verbose/actions/workflows/test-python.yml) [![Upload Python Package](https://github.com/ccmorenos/pretty_verbose/actions/workflows/python-publish.yml/badge.svg)](https://github.com/ccmorenos/pretty_verbose/actions/workflows/python-publish.yml)

Package for beautiful verbose printing in python.

## Installation

The package is available in the [Python Package Index (PyPi)](https://pypi.org/project/pretty-verbose/).

```bash
python3 -m pip install pretty_verbose
```

## Examples

### Simple output

To use the verbose output, create a `VerboseMessages` object.

```python
from pretty_verbose import VerboseMessages

messages = VerboseMessages(
    level=3,
    name="main",
    filename="messages.log",
    log_dir="path/to/log_dir"  # Optional for saving the log in the given dir.
)
```

The level indicates which messages will be printed.

* -1: Just Debug.
* 0: Debug and Errors.
* 1: Debug, Errors and Warnings.
* 2: Debug, Errors Warnings and Success.
* 3: Debug, Errors Warnings, Success and Info.

The name works to use the VerboseMessages in several instance and
differentiate where the message is coming from. Finally the filename will store
all the messages printed in the terminal.

The following messages can be printed.

```python
import time

messages.debug("This is a debug message.")
messages.error("This is an error message.")
messages.warning("This is a warning message.")
messages.success("This is a success message.")
messages.info("This is an info message.")

for i in range(100):
    if i % 10 == 0:
        messages.for_message("This is an info message inside a for loop.")
    messages.progress("This is a progress message.", (i+1))
    time.sleep(0.1)
```

The result will be the following.

```
[28/08/2022 14:12:09] DEBUG [main]: This is an debug message.
[28/08/2022 14:12:09] ERROR [main]: This is an error message.
[28/08/2022 14:12:09] WARNING [main]: This is a warning message.
[28/08/2022 14:12:09] SUCCESS [main]: This is a success message.
[28/08/2022 14:14:06] SUCCESS [main]: This is a success message.
[28/08/2022 14:12:10] INFO [main] -- This is an info message inside a for loop.
[28/08/2022 14:12:11] INFO [main] -- This is an info message inside a for loop.
[28/08/2022 14:12:13] INFO [main] -- This is an info message inside a for loop.
[28/08/2022 14:12:14] INFO [main] -- This is an info message inside a for loop.
[28/08/2022 14:12:15] INFO [main] -- This is an info message inside a for loop.
[28/08/2022 14:12:16] INFO [main] -- This is an info message inside a for loop.
[28/08/2022 14:12:17] INFO [main] -- This is an info message inside a for loop.
[28/08/2022 14:12:18] INFO [main] -- This is an info message inside a for loop.
[28/08/2022 14:12:19] INFO [main] -- This is an info message inside a for loop.
[28/08/2022 14:12:20] INFO [main] -- This is an info message inside a for loop.
[28/08/2022 14:14:19] INFO [main] -- This is a progress message.: [100.00%]
```

### Tasks and Processes

There are more complete classes such as `Task` and `Process` that allow
measurement of execution time as well as creating subordinate verbose messages.
Both are equipped with all the printing function as they are inherited from the
`VerboseMessages` class.

With `Task` it is possible to measure how long it takes to complete a execution of a function:

```python
task1 = Task(level=5, name="task1")

ex_time = task1.exec_time(
    some_callable,  # Function from which measure the execution time.
    arg1, arg2,  # Arguments of the function.
    print_timer=True  # Print the time execution as it just return it.
)
ex_time = task1.exec_many_time(
    callable1, callable2, callable3,  # Functions from which measure the execution time.
    [[f1_arg1, f1_arg2], [], [f3_arg1]], # Arguments of the functions.
    print_timer=True  # Print the time execution as it just return it.
)
```

Additionally it is possible just to activate, deactivate, get the partial and
total time of the timer.

```python
task1.start_timer()

# ...some code ...
lap_time = task1.lap()

# ...some code ...
task1.print_lap()

# ...some code ...
task1.stop_timer()

total_t = task1.total_time()
```

With `Process` it is possible to create subtasks and subprocesses associated to
it.

```python
main_process = Process(level=5, name="main")

subprocess_1: Process = main_process.new_subprocess("subprocess_1")
subprocess_2: Process = main_process.new_subprocess("subprocess_2")
subtask_2: Task = main_process.new_task("subtask_1")

# Subprocess as they are Process object, they can also create new processes and
# tasks.
subsubprocess_1: Process = subprocess_1.new_subprocess("subsubprocess_1")
subsubtask_2: Task = subprocess_1.new_task("subsubtask_1")
```

All the `Process` objects are also equipped with the timer functions as it
inherits from the `Task` class.
