import prof
import os

on_message = False

def prof_on_message_received(jid, message):
    if on_message:
        os.system("say \"" + jid + " says " + message + "\" 2>/dev/null")    
    return message

def prof_on_room_message_received(room, nick, message):
    if on_message:
        os.system("say \"" + nick + " says " + message + " in " + room + "\" 2>/dev/null")    
    return message

def prof_on_private_message_received(room, nick, message):
    if on_message:
        os.system("say \"" + nick + " says " + message + "\" 2>/dev/null")    
    return message

def _cmd_say(msg=None):
    if msg: 
        os.system("say \"" + msg + "\" &2>/dev/null")    

def prof_init(version, status):
    prof.register_command("/say", 0, 1, "/say message", "Say something.", "Say something.",
        _cmd_say)
