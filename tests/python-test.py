import prof

plugin_win = "Python Test"

def _handle_win_input(win, line):
    prof.win_show(win, "Input received: " + line)

def create_win():
    if prof.win_exists(plugin_win) == False:
        prof.win_create(plugin_win, _handle_win_input)

def cmd_pythontest(arg1=None, arg2=None, arg3=None):
    if arg1 == "consalert":
        create_win()
        prof.win_focus(plugin_win)
        prof.cons_alert()
        prof.win_show(plugin_win, "called -> prof.cons_alert")
    elif arg1 == "consshow":
        if arg2 != None:
            create_win()
            prof.win_focus(plugin_win)
            prof.cons_show(arg2)
            prof.win_show(plugin_win, "called -> prof.cons_show: " + arg2)
        else:
            prof.cons_bad_cmd_usage("/python-test")
    elif arg1 == "sendline":
        if arg2 != None:
            create_win()
            prof.win_focus(plugin_win)
            prof.send_line(arg2)
            prof.win_show(plugin_win, "called -> prof.send_line: " + arg2)
        else:
            prof.cons_bad_cmd_usage("/python-test")
    elif arg1 == "notify":
        if arg2 != None:
            create_win()
            prof.win_focus(plugin_win)
            prof.notify(arg2, 5000, "python-test plugin")
            prof_win_show(plugin_win, "called -> prof.notify: " + arg2)
        else:
            prof.cons_bad_cmd_usage("/python-test")
    elif arg1 == "get":
        if arg2 == None:
            prof.cons_bad_cmd_usage("/python-test")
        elif arg2 == "recipient":
            create_win()
            recipient = prof.get_current_recipient();
            if recipient != None:
                prof.win_focus(plugin_win)
                prof.win_show(plugin_win, "called -> prof.get_current_recipient: " + recipient)
            else:
                prof.win_focus(plugin_win)
                prof.win_show(plugin_win, "called -> prof_get_current_recipient: <none>")
        elif arg2 == "room":
            create_win()
            room = prof.get_current_muc()
            if room != None:
                prof.win_focus(plugin_win)
                prof.win_show(plugin_win, "called -> prof_get_current_muc: " + room)
            else:
                prof.win_focus(plugin_win)
                prof.win_show(plugin_win, "called -> prof_get_current_muc: <none>")
        else:
            prof.cons_bad_cmd_usage("/python-test")
    elif arg1 == "log":
        if arg2 == None:
            prof.cons_bad_cmd_usage("/python-test")
        elif arg2 == "debug":
            if arg3 == None:
                prof.cons_bad_cmd_usage("/python-test")
            else:
                create_win()
                prof.win_focus(plugin_win)
                prof.log_debug(arg3)
                prof.win_show(plugin_win, "called -> prof.log_debug: " + arg3)
        elif arg2 == "info":
            if arg3 == None:
                prof.cons_bad_cmd_usage("/python-test")
            else:
                create_win()
                prof.win_focus(plugin_win)
                prof.log_info(arg3)
                prof.win_show(plugin_win, "called -> prof.log_info: " + arg3)
        elif arg2 == "warning":
            if arg3 == None:
                prof.cons_bad_cmd_usage("/python-test")
            else:
                create_win()
                prof.win_focus(plugin_win)
                prof.log_warning(arg3)
                prof.win_show(plugin_win, "called -> prof.log_warning: " + arg3)
        elif arg2 == "error":
            if arg3 == None:
                prof.cons_bad_cmd_usage("/python-test")
            else:
                create_win()
                prof.win_focus(plugin_win)
                prof.log_error(arg3)
                prof.win_show(plugin_win, "called -> prof.log_error: " + arg3)
        else:
            prof.cons_bad_cmd_usage("/c-test")
    else:
        prof.cons_bad_cmd_usage("/c-test")

def prof_init(version, status):
    prof.win_create(plugin_win, _handle_win_input)

    synopsis = [
        "/python-test consalert",
        "/python-test consshow <message>",
        "/python-test notify <message>",
        "/python-test sendline <line>",
        "/python-test get recipient|room",
        "/python-test log debug|info|warning|error <message>"
    ]
    description = "Python test plugins. All commands focus the plugin window."
    args = [
        [ "consalert",                              "Highlight the console window in the status bar" ],
        [ "consshow <message>",                     "Show the message in the console window" ],
        [ "notify <message>",                       "Send a desktop notification with message" ],
        [ "sendline <line>",                        "Pass line to profanity to process" ],
        [ "get recipient",                          "Show the current chat recipient, if in a chat window" ],
        [ "get room",                               "Show the current room JID, if ina a chat room"],
        [ "log debug|info|warning|error <message>", "Log a message at the specified level" ]
    ]
    examples = [
        "/python-test sendline /about",
        "/python-test log debug \"Test debug message\""
    ]

    prof.register_command("/python-test", 1, 3, synopsis, description, args, examples, cmd_pythontest)

    prof.register_ac("/python-test", 
        [ "consalert", "consshow", "notify", "sendline", "get", "log" ]
    )
    prof.register_ac("/python-test get",
        [ "recipient", "room" ]
    )
    prof.register_ac("/python-test log",
        [ "debug", "info", "warning", "error" ]
    )

def prof_on_start():
    create_win()
    prof.win_show(plugin_win, "fired -> prof_on_start")

def prof_on_shutdown():
    create_win()
    prof.win_show(plugin_win, "fired -> prof_on_shutdown")

def prof_on_connect(account_name, fulljid):
    create_win()
    prof.win_show(plugin_win, "fired -> prof_on_connect: " + account_name + ", " + fulljid)

def prof_on_disconnect(account_name, fulljid):
    create_win()
    prof.win_show(plugin_win, "fired -> prof_on_disconnect: " + account_name + ", " + fulljid)

def prof_pre_chat_message_display(jid, message):
    create_win()
    prof.win_show(plugin_win, "fired -> prof_pre_chat_message_display: " + jid + ", " + message)

def prof_post_chat_message_display(jid, message):
    create_win()
    prof.win_show(plugin_win, "fired -> prof_post_chat_message_display: " + jid + ", " + message)

def prof_pre_chat_message_send(jid, message):
    create_win()
    prof.win_show(plugin_win, "fired -> prof_pre_chat_message_send: " + jid + ", " + message)

def prof_post_chat_message_send(jid, message):
    create_win()
    prof.win_show(plugin_win, "fired -> prof_post_chat_message_send: " + jid + ", " + message)

def prof_pre_room_message_display(room, nick, message):
    create_win()
    prof.win_show(plugin_win, "fired -> prof_pre_room_message_display: " + room + ", " + nick + ", " + message)

def prof_post_room_message_display(room, nick, message):
    create_win()
    prof.win_show(plugin_win, "fired -> prof_post_room_message_display: " + room + ", " + nick + ", " + message)

def prof_pre_room_message_send(room, message):
    create_win()
    prof.win_show(plugin_win, "fired -> prof_pre_room_message_send: " + room + ", " + message)

def prof_post_room_message_send(room, message):
    create_win()
    prof.win_show(plugin_win, "fired -> prof_post_room_message_send: " + room + ", " + message)

def prof_pre_priv_message_display(room, nick, message):
    create_win()
    prof.win_show(plugin_win, "fired -> prof_pre_priv_message_display: " + room + ", " + nick + ", " + message)

def prof_post_priv_message_display(room, nick, message):
    create_win()
    prof.win_show(plugin_win, "fired -> prof_post_priv_message_display: " + room + ", " + nick + ", " + message)

def prof_pre_priv_message_send(room, nick, message):
    create_win()
    prof.win_show(plugin_win, "fired -> prof_pre_priv_message_send: " + room + ", " + nick + ", " + message)

def prof_post_priv_message_send(room, nick, message):
    create_win()
    prof.win_show(plugin_win, "fired -> prof_post_priv_message_send: " + room + ", " + nick + ", " + message)

