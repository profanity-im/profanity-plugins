import prof

def _emote(input_str):
    result = input_str
    result = result.replace(":-)", u'\u263a'.encode("utf-8"))
    result = result.replace(":)", u'\u263a'.encode("utf-8"))
    result = result.replace(":-(", u'\u2639'.encode("utf-8"))
    result = result.replace(":(", u'\u2639'.encode("utf-8"))
    return result

def prof_pre_chat_message_display(jid, message):
    return _emote(message)

def prof_pre_room_message_display(room, nick, message):
    return _emote(message)

def prof_pre_priv_message_display(room, nick, message):
    return _emote(message)
