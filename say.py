import prof
import os

enabled = False

def prof_post_chat_message_display(jid, message):
    global enabled
    if enabled:
        os.system("say \"" + jid + " says " + message + "\" 2>/dev/null")    
    return message

def prof_post_room_message_display(room, nick, message):
    global enabled
    if enabled:
        os.system("say \"" + nick + " says " + message + " in " + room + "\" 2>/dev/null")    
    return message

def prof_post_priv_message_display(room, nick, message):
    global enabled
    if enabled:
        os.system("say \"" + nick + " says " + message + "\" 2>/dev/null")    
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
    prof.register_command("/say", 1, 1, "/say on|pff", "Enable or disable say.", "Enable or disable say.",
        _cmd_say)
    prof.register_ac("/say", [ "on", "off" ])
