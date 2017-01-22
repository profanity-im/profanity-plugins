import prof

chat_msg_hook = None
room_msg_hook = None

def _cmd_enc(arg1=None, arg2=None, arg3=None, arg4=None, arg5=None):
    global chat_msg_hook
    global room_msg_hook

    if arg1 == "end":
        prof.encryption_reset(arg2)

    elif arg1 == "chat_title" and arg2 == "set":
        prof.chat_set_titlebar_enctext(arg3, arg4)

    elif arg1 == "chat_title" and arg2 == "reset":
        prof.chat_unset_titlebar_enctext(arg3)

    elif arg1 == "chat_ch" and arg2 == "set" and arg3 == "in":
        prof.chat_set_incoming_char(arg4, arg5)

    elif arg1 == "chat_ch" and arg2 == "reset" and arg3 == "in":
        prof.chat_unset_incoming_char(arg4)

    elif arg1 == "chat_ch" and arg2 == "set" and arg3 == "out":
        prof.chat_set_outgoing_char(arg4, arg5)

    elif arg1 == "chat_ch" and arg2 == "reset" and arg3 == "out":
        prof.chat_unset_outgoing_char(arg4)

    elif arg1 == "room_title" and arg2 == "set":
        prof.room_set_titlebar_enctext(arg3, arg4)

    elif arg1 == "room_title" and arg2 == "reset":
        prof.room_unset_titlebar_enctext(arg3)

    elif arg1 == "room_ch" and arg2 == "set":
        prof.room_set_message_char(arg3, arg4)

    elif arg1 == "room_ch" and arg2 == "reset":
        prof.room_unset_message_char(arg3)

    elif arg1 == "chat_show":
        prof.chat_show(arg2, arg3)

    elif arg1 == "chat_show_themed":
        prof.chat_show_themed(arg2, "enc_py", "chat_msg", None, "p", arg3)

    elif arg1 == "room_show":
        prof.room_show(arg2, arg3)

    elif arg1 == "room_show_themed":
        prof.room_show_themed(arg2, "enc_py", "room_msg", None, "P", arg3)

    elif arg1 == "chat_msg":
        chat_msg_hook = arg2

    elif arg1 == "room_msg":
        room_msg_hook = arg2

    else:
        prof.cons_bad_cmd_usage("/enc_py")


def prof_init(version, status, account_name, fulljid):
    synopsis = [ 
        "/enc_py end <barejid>",
        "/enc_py chat_title set <barejid> <text>",
        "/enc_py chat_title unset <barejid>",
        "/enc_py chat_ch set in <barejid> <ch>",
        "/enc_py chat_ch reset in <barejid>",
        "/enc_py chat_ch set out <barejid> <ch>",
        "/enc_py chat_ch reset out <barejid>",
        "/enc_py chat_show <barejid> <message>",
        "/enc_py chat_show_themed <barejid> <message>",
        "/enc_py room_title set <roomjid> <text>",
        "/enc_py room_title unset <roomjid>"
        "/enc_py room_ch set <roomjid> <ch>",
        "/enc_py room_ch reset <roomjid>",
        "/enc_py room_show <roomjid> <message>",
        "/enc_py room_show_themed <roomjid> <message>"
        "/enc_py chat_msg none",
        "/enc_py chat_msg modify",
        "/enc_py chat_msg block",
        "/enc_py room_msg none",
        "/enc_py room_msg modify",
        "/enc_py room_msg block"
    ]
    description = "Various enc things"
    args = [
        [ "end <barejid>",                          "User to end the session with" ],
        [ "chat_title set <barejid> <text>",        "Set encryption text in titlebar for recipient" ],
        [ "chat_title reset <barejid>",             "Reset encryption text in titlebar for recipient" ],
        [ "chat_ch set in <barejid> <ch>",          "Set incoming char for recipient" ],
        [ "chat_ch reset in <barejid>",             "Reset incoming char for recipient" ],
        [ "chat_ch set out <barejid> <ch>",         "Set outgoing char for recipient" ],
        [ "chat_ch reset out <barejid>",            "Reset outgoing char for recipient" ],
        [ "chat_show <barejid> <message>",          "Show chat message" ],
        [ "chat_show_themed <barejid> <message>",   "Show themed chat message" ],
        [ "room_title set <roomjid> <text>",        "Set encryption text in titlebar for room" ],
        [ "room_title reset <roomjid>",             "Reset encryption text in titlebar for room" ],
        [ "room_ch set <roomjid> <ch>",             "Set char for room" ],
        [ "room_ch reset <roomjid>",                "Reset char for room" ],
        [ "room_show <roomjid> <message>",          "Show chat room message" ],
        [ "room_show_themed <roomjid> <message>",   "Show themed chat room message" ],
        [ "chat_msg none",                          "Preserve chat messages" ],
        [ "chat_msg modify",                        "Modify chat messages" ],
        [ "chat_msg block",                         "Block chat messages" ],
        [ "room_msg none",                          "Preserve chat room messages" ],
        [ "room_msg modify",                        "Modify chat room messages" ],
        [ "room_msg block",                         "Block chat room messages" ]
    ]
    examples = []

    prof.register_command("/enc_py", 2, 5, synopsis, description, args, examples, _cmd_enc)
    prof.completer_add("/enc_py", [
        "end",
        "chat_title",
        "chat_ch",
        "chat_show",
        "chat_show_themed",
        "room_title",
        "room_ch",
        "room_show",
        "room_show_themed",
        "chat_msg",
        "room_msg"
    ])
    prof.completer_add("/enc_py chat_title", [ "set", "reset" ])
    prof.completer_add("/enc_py chat_ch", [ "set", "reset" ])
    prof.completer_add("/enc_py chat_ch set", [ "in", "out" ])
    prof.completer_add("/enc_py chat_ch reset", [ "in", "out" ])
    prof.completer_add("/enc_py room_title", [ "set", "reset" ])
    prof.completer_add("/enc_py room_ch", [ "set", "reset" ])
    prof.completer_add("/enc_py chat_msg", [ "none", "modify", "block" ])
    prof.completer_add("/enc_py room_msg", [ "none", "modify", "block" ])


def prof_pre_chat_message_send(barejid, message):
    if chat_msg_hook == "modify":
        return "[py modified] " + message
    elif chat_msg_hook == "block":
        prof.chat_show_themed(barejid, None, None, "bold_red", "!", "Python plugin blocked message")
        return None
    else:
        prof.log_info("none")
        return message


def prof_pre_room_message_send(roomjid, message):
    if room_msg_hook == "modify":
        return "[py modified] " + message
    elif room_msg_hook == "block":
        prof.room_show_themed(roomjid, None, None, "bold_red", "!", "Python plugin blocked message")
        return None
    else:
        return message
