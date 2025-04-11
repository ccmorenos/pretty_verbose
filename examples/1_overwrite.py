"""This example test the overwriting functionality."""
import time

from pretty_verbose import VerboseMessages


def write_log(ow):
    messages = VerboseMessages(
        level=3,
        scope="test",
        filename="overwrite.log",
        log_dir="log_output",
        overwrite=ow
    )

    messages.success(f"Overwrite: {ow}.")

    messages.debug("This is a debug message.")
    messages.error("This is an error message.")
    messages.warning("This is a warning message.")
    messages.success("This is a success message.")
    messages.info("This is an info message.")

    for i in range(50):
        if i % 10 == 0:
            messages.for_message("This is an info message inside a for loop.")
        messages.progress("This is a progress message.", (i+1)/0.5)
        time.sleep(0.01)
    messages.end_progress("Loop.")

    user_input = messages.input("Hola")
    messages.info("You answered: " + user_input)

    b_continue = messages.confirm("New try", "Do you want to continue?")

    messages.info(f"You continued: {b_continue}")

    return b_continue


overwrite = True

while True:
    if write_log(overwrite):
        overwrite = not overwrite
    else:
        break
