"""This example test the logger classes and functionalities."""
import time
from random import random

from pretty_verbose import Logger


def test_prints(messager):
    """Teste de messager prints."""
    messager.success("Created")
    messager.debug("This is a debug message.")
    messager.error("This is an error message.")
    messager.warning("This is a warning message.")
    messager.success("This is a success message.")
    messager.info("This is an info message.")

    for i in range(100):
        messager.progress("Testing time", (i+1))
        time.sleep(random()*0.01)

    messager.success(f"Done in {messager.lap()} ms")


def stop(messager):
    """Stop the messager."""
    messager.stop_timer()
    messager.success(f"Task done in {main.total_time()} ms")


main = Logger(5, "Main", ".logger", "main.log")

sub1 = main.new_subprocess("Sub1", "sub1.log")
sub2 = main.new_subprocess("Sub2", "sub2.log")

test_prints(main)
test_prints(sub1)
test_prints(sub2)

stop(main)
stop(sub1)
stop(sub2)
