"""This example test the processes classes and functionalities."""
import time
from random import random

from pretty_verbose import Process


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


main = Process(5, "Main", "log_output", timer=True, overwrite=True)
test_prints(main)

sp1: Process = main.new_subprocess("Sub 1", timer=True)
test_prints(sp1)

sp2: Process = main.new_subprocess("Sub 2", timer=True)
test_prints(sp2)

ssp1: Process = sp2.new_subprocess("SSub 1", timer=True)
test_prints(ssp1)

sssp1: Process = ssp1.new_subprocess("SSSub 1", timer=True)
test_prints(sssp1)

tsk1 = sp2.new_task("Task 1", timer=True)
test_prints(tsk1)

stsk1 = ssp1.new_task("STask 1", timer=True)
test_prints(stsk1)

stop(main)
stop(sp1)
stop(sp2)
stop(ssp1)
stop(sssp1)
stop(tsk1)
stop(stsk1)
