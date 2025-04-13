import time

from pretty_verbose import VerboseMessages

messages = VerboseMessages(
    level=3,
    scope="test",
    filename="messages.log",
    log_dir="log_output"
)

messages.debug("This is a debug message.")
messages.error("This is an error message.")
messages.warning("This is a warning message.")
messages.success("This is a success message.")
messages.info("This is an info message.")

rep = 50
for i in range(rep):
    if i % 10 == 0:
        messages.for_message("This is an info message inside a for loop.")
    messages.progress("This is a progress message.", (i+1)/rep*100)
    time.sleep(0.01)
messages.end_progress("Loop.")


messages.debug("This ", "is ", "a ", "debug ", "message.")
messages.debug("Trying numbers", 0, 1, 0.1)
messages.debug("Trying lists", ["A", 0, 1.5])

messages.error("This ", "is ", "a ", "error ", "message.")
messages.error("Trying numbers", 0, 1, 0.1)
messages.error("Trying lists", ["A", 0, 1.5])

messages.warning("This ", "is ", "a ", "warning ", "message.")
messages.warning("Trying numbers", 0, 1, 0.1)
messages.warning("Trying lists", ["A", 0, 1.5])

messages.success("This ", "is ", "a ", "success ", "message.")
messages.success("Trying numbers", 0, 1, 0.1)
messages.success("Trying lists", ["A", 0, 1.5])

messages.info("This ", "is ", "a ", "info ", "message.")
messages.info("Trying numbers", 0, 1, 0.1)
messages.info("Trying lists", ["A", 0, 1.5])

user_input = messages.input("Hola")
messages.info("You answered: " + user_input)

b_continue = messages.confirm("Confirm message", "Do you want to continue?")

messages.info(f"You continued: {b_continue}")

letter = messages.select("Letters", options=["a", "b", "c"])
messages.info(f"You selected: {letter}")

number = messages.select("Numbers", options=[i*2+3 for i in range(1, 11, 2)])
messages.info(f"You selected: {number}")

many = messages.select(
    "Many", options=[i*2+3 for i in range(1, 11, 2)], many=True
)
messages.info(f"You selected: {many}")
