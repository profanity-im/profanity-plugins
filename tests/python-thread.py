import prof
import threading
import time
import sys

counter = 0

def _inc_counter():
    global counter
    while True:
        time.sleep(1)
        counter = counter + 1
    
def _cmd_count():
    prof.cons_show("Counter: " + str(counter))

def prof_init(version, status):
    t = threading.Thread(target=_inc_counter)
    t.daemon = True
    t.start()

    synopsis = [ "/count" ]
    description = "Python threading example."
    args = []
    examples = []

    prof.register_command("/count", 0, 0, synopsis, description, args, examples, _cmd_count)
