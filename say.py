import prof
import os

on_message = True

def prof_post_chat_message_display(jid, message):
    if on_message:
        os.system("say \"" + jid + " says " + message + "\" 2>/dev/null")    
    return message

def prof_post_room_message_display(room, nick, message):
    if on_message:
        os.system("say \"" + nick + " says " + message + " in " + room + "\" 2>/dev/null")    
    return message

def prof_post_priv_message_display(room, nick, message):
    if on_message:
        os.system("say \"" + nick + " says " + message + "\" 2>/dev/null")    
    return message

def _cmd_say(msg=None):
    if msg: 
        os.system("say \"" + msg + "\" 2>/dev/null")    

def prof_init(version, status):
    prof.register_command("/say", 0, 1, "/say message", "Say something.", "Say something.",
        _cmd_say)
