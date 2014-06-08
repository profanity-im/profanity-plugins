import prof
import os

def prof_on_message_received(jid, message):
    os.system("say \"" + jid + " says " + message + "\" 2>/dev/null")    
    return message

def prof_on_room_message_received(room, nick, message):
    os.system("say \"" + nick + " says " + message + " in " + room + "\" 2>/dev/null")    
    return message

def prof_on_private_message_received(room, nick, message):
    os.system("say \"" + nick + " says " + message + "\" 2>/dev/null")    
    return message
