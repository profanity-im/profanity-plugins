import prof

def emote(input_str):
    result = input_str
    result = result.replace(":-)", u'\u263a')
    result = result.replace(":)", u'\u263a')
    result = result.replace(":-(", u'\u2639')
    result = result.replace(":(", u'\u2639')
    return result


def prof_before_message_displayed(message):
    return emote(message)
