"""
Converts smileys in a text to their Unicode character representations.
"""

import prof

EMOTICON_UNICODE_DICT = {':)': '😃', ':(': '☹️', ':D': '😃', ':O': '😲', ';)': '😉', ':-)': '😊', ':-D': '😁', ':-(': '😞',
                         ';-)': '😜', '<3': '❤️', ':P': '😛', ':|': '😐', ':/': '😕', ':*': '😘', ':]': '😃', ':[': '😢',
                         ':-|': '😐', ':\\': '😕', ':3': '😺', 'O:)': '😇', '>:(': '😠', ':poop:': '💩', ':fire:': '🔥',
                         ':heart:': '❤️', ':thumbsup:': '👍', ':star:': '⭐', ':beer:': '🍺', ':pizza:': '🍕', ':sunglasses:': '😎',
                         ':ok_hand:': '👌', ':heart_eyes:': '😍'}


def replace_emoticons(text, emoticon_dict):
    for emoticon, unicode_char in emoticon_dict.items():
        text = text.replace(emoticon, unicode_char)
    return text


def convert_emoticons(input_str):
    return replace_emoticons(input_str, EMOTICON_UNICODE_DICT)


def prof_pre_chat_message_display(barejid, resource, message):
    return convert_emoticons(message)


def prof_pre_room_message_display(barejid, nick, message):
    return convert_emoticons(message)


def prof_pre_priv_message_display(barejid, nick, message):
    return convert_emoticons(message)
