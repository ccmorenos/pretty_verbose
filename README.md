# Pretty Verbose
[![PyPI version](https://img.shields.io/pypi/v/pretty-verbose.svg)](https://pypi.org/project/pretty-verbose/)
[![License](https://img.shields.io/pypi/l/pretty-verbose.svg)](https://github.com/ccmorenos/pretty_verbose/blob/main/LICENSE)
[![Test Python Package](https://github.com/ccmorenos/pretty_verbose/actions/workflows/test-python.yml/badge.svg?branch=main)](https://github.com/ccmorenos/pretty_verbose/actions/workflows/test-python.yml) [![Upload Python Package](https://github.com/ccmorenos/pretty_verbose/actions/workflows/python-publish.yml/badge.svg)](https://github.com/ccmorenos/pretty_verbose/actions/workflows/python-publish.yml)

Package for beautiful verbose printing in python.

## Installation

The package is available in the [Python Package Index (PyPi)](https://pypi.org/project/pretty-verbose/).

```bash
python3 -m pip install pretty_verbose
```

## Examples

To use the verbose output, create a `VerboseMessages` object.

```python
from pretty_verbose import VerboseMessages

messages = VerboseMessages(
    level=3,
    scope="main",
    filename="messages.log"
)
```

The level indicates which messages will be printed.

* -1: Just Debug.
* 0: Debug and Errors.
* 1: Debug, Errors and Warnings.
* 2: Debug, Errors Warnings and Success.
* 3: Debug, Errors Warnings, Success and Info.

The scope works to use the VerboseMessages in several instance and
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
