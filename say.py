"""
Read message out loud.

On linux requires 'espeak' which is available on most distributions e.g.:
    sudo apt-get install espeak

On OSX will use the built in 'say' command.
"""

import prof
import os
from sys import platform

enabled = False

def say(message):
    if platform == "darwin":
        os.system("say '" + message + "' 2>/dev/null")
    elif platform == "linux" or platform == "linux2":
        os.system("echo '" + message + "' | espeak 2>/dev/null")

def prof_post_chat_message_display(jid, message):
    global enabled
    if enabled:
        say(jid + " says " + message)
    return message

def prof_post_room_message_display(room, nick, message):
    global enabled
    if enabled:
        say(nick + " says " + message + " in " + room)
    return message

def prof_post_priv_message_display(room, nick, message):
    global enabled
    if enabled:
        say(nick + " says " + message)
    return message

def _cmd_say(arg1=None, arg2=None):
    global enabled
    if arg1 == "on":
        enabled = True
    elif arg1 == "off":
        enabled = False
    elif arg1 == "test":
        if arg2 == None:
            prof.cons_bad_cmd_usage("/say")
        else:
            say(arg2)
    else:
        prof.cons_bad_cmd_usage("/say")

def prof_init(version, status):
    synopsis = [ 
        "/say on|off",
        "/say test <message>"
    ]
    description = "Read all messages out loud"
    args = [
        [ "on|off",         "Enable/disable say" ],
        [ "test <message>", "Say message" ]
    ]
    examples = []

    prof.register_command("/say", 1, 2, synopsis, description, args, examples, _cmd_say)
    prof.register_ac("/say", [ "on", "off", "test" ])
