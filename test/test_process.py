"""Test the task class."""
import time
from random import random

from pretty_verbose import Process

process = Process(3, "test", log_file="messages.log")


def test_debug_message():
    """Test debug message printing."""
    process.debug("This is a debug message.")


def test_error_message():
    """Test error message printing."""
    process.error("This is an error message.")


def test_warning_message():
    """Test warning message printing."""
    process.warning("This is a warning message.")


def test_success_message():
    """Test success message printing."""
    process.success("This is a success message.")


def test_info_message():
    """Test info message printing."""
    process.info("This is an info message.")


def test_for_message():
    """Test info message printing in a for loop."""
    for i in range(50):
        if i % 10 == 0:
            process.for_message("This is an info message inside a for loop.")
        process.progress("This is a progress message.", (i+1))
        time.sleep(0.01)
    process.end_progress("Loop.")


def test_multiple_messages():
    """Test debug message printing."""
    process.debug("This ", "is ", "a ", "debug ", "message.")
    process.debug("Trying numbers", 0, 1, 0.1)
    process.debug("Trying lists", ["A", 0, 1.5])


def test_prints(messager=process):
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


def test_timer():
    """Test timer starting, lap and stopping."""
    process.start_timer()
    test_prints()
    process.end_progress("Loop.")
    process.stop_timer()


def test_subprocess():
    """Test debug message printing."""
    sp1: Process = process.new_subprocess("Sub1", timer=True)
    ssp1: Process = sp1.new_subprocess("SubSub1", timer=True)
    tsk1: Process = sp1.new_task("Task1", timer=True)

    test_prints(sp1)
    test_prints(ssp1)
    test_prints(tsk1)

    sp1.stop_timer()
    ssp1.stop_timer()
    tsk1.stop_timer()
