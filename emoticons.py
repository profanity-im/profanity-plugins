"""
Convert smileys ( :) :( etc) to the Unicode character representation
"""

import prof
from builtins import chr


def _emote(input_str):
    result = input_str
    result = result.replace(":-)", chr(9786))
    result = result.replace(":)", chr(9786))
    result = result.replace(":-(", chr(9785))
    result = result.replace(":(", chr(9785))
    return result


def prof_pre_chat_message_display(jid, message):
    return _emote(message)


def prof_pre_room_message_display(room, nick, message):
    return _emote(message)


def prof_pre_priv_message_display(room, nick, message):
    return _emote(message)
