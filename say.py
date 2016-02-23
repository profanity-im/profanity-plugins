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

def _cmd_say(arg=None):
    global enabled
    if arg == "on":
        enabled = True
    elif arg == "off":
        enabled = False
    else:
        prof.cons_show("Usage: /say on|off")

def prof_init(version, status):
    synopsis = [ 
        "/say on|off"
    ]
    description = "Read all messages out loud"
    args = [
        [ "on|off", "Enable/disable say" ]
    ]
    examples = []

    prof.register_command("/say", 1, 1, synopsis, description, args, examples, _cmd_say)
    prof.register_ac("/say", [ "on", "off" ])
