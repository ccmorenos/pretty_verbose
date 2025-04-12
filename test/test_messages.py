"""Test the messages printing."""
import time

from pretty_verbose import VerboseMessages

messages = VerboseMessages(
    level=3,
    scope="test",
    filename="messages.log"
)


def test_debug_message():
    """Test debug message printing."""
    messages.debug("This is a debug message.")


def test_error_message():
    """Test error message printing."""
    messages.error("This is an error message.")


def test_warning_message():
    """Test warning message printing."""
    messages.warning("This is a warning message.")


def test_success_message():
    """Test success message printing."""
    messages.success("This is a success message.")


def test_info_message():
    """Test info message printing."""
    messages.info("This is an info message.")


def test_for_message():
    """Test info message printing in a for loop."""
    for i in range(50):
        if i % 10 == 0:
            messages.for_message("This is an info message inside a for loop.")
        messages.progress("This is a progress message.", (i+1))
        time.sleep(0.01)
    messages.end_progress("Loop.")


def test_multiple_messages():
    """Test debug message printing with multiple entries."""
    messages.debug("This ", "is ", "a ", "debug ", "message.")
    messages.debug("Trying numbers", 0, 1, 0.1)
    messages.debug("Trying lists", ["A", 0, 1.5])
