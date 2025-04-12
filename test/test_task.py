"""Test the task class."""
import time

from pretty_verbose import Task

task = Task(3, "test", log_file="messages.log")


def test_debug_message():
    """Test debug message printing."""
    task.debug("This is a debug message.")


def test_error_message():
    """Test error message printing."""
    task.error("This is an error message.")


def test_warning_message():
    """Test warning message printing."""
    task.warning("This is a warning message.")


def test_success_message():
    """Test success message printing."""
    task.success("This is a success message.")


def test_info_message():
    """Test info message printing."""
    task.info("This is an info message.")


def test_for_message():
    """Test info message printing in a for loop."""
    for i in range(50):
        if i % 10 == 0:
            task.for_message("This is an info message inside a for loop.")
        task.progress("This is a progress message.", (i+1))
        time.sleep(0.01)
    task.end_progress("Loop.")


def test_multiple_messages():
    """Test debug message printing with multiple entries."""
    task.debug("This ", "is ", "a ", "debug ", "message.")
    task.debug("Trying numbers", 0, 1, 0.1)
    task.debug("Trying lists", ["A", 0, 1.5])


def test_timer():
    """Test timer starting, lap and stopping."""
    task.start_timer()
    for i in range(100):
        if i % 10 == 0:
            task.for_message("This is an info message inside a for loop.")
        task.progress("This is a progress message.", (i+1))
        time.sleep(0.1)

        task.print_lap()

    task.end_progress("Loop.")
    task.stop_timer()
