"""
Print something in ASCII text.
Running from the console will print the text to the console.
Running in a chat or room window will send the ASCII text

Requires 'figlet' which is available on most linux distros e.g.:
    sudo apt-get install figlet
"""

import prof
import subprocess


def _cmd_ascii(text):
    proc = subprocess.Popen(['figlet', '--', text], stdout=subprocess.PIPE)
    ascii_out = proc.communicate()[0].decode('utf-8')
    recipient = prof.get_current_recipient()
    room = prof.get_current_muc()
    if recipient:
        prof.send_line(u'\u000A' + ascii_out)
    elif room:
        prof.send_line(u'\u000A' + ascii_out)
    elif prof.current_win_is_console():
        prof.cons_show(u'\u000A' + ascii_out)


def prof_init(version, status, account_name, fulljid):
    synopsis = [ "/ascii <message>" ]
    description = "ASCIIfy a message."
    args = [
        [ "<message>", "The message to be ASCIIfied" ]
    ]
    examples = [
        "/ascii \"Hello there\""
    ]
    
    prof.register_command("/ascii", 1, 1, synopsis, description, args, examples, _cmd_ascii)
