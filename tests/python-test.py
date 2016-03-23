import prof

import threading
import time

plugin_win = "Python Test"

count = 0
ping_id = 1

def _inc_counter():
    global count
    while True:
        time.sleep(5)
        count = count + 1

def _handle_win_input(win, line):
    prof.win_show(win, "Input received: " + line)

def create_win():
    if prof.win_exists(plugin_win) == False:
        prof.win_create(plugin_win, _handle_win_input)

def cmd_pythontest(arg1=None, arg2=None, arg3=None, arg4=None, arg5=None):
    global ping_id
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
    elif arg1 == "consshow_t":
        if arg2 == None or arg3 == None or arg4 == None or arg5 == None:
            prof.cons_bad_cmd_usage("/python-test");
        else:
            group = None if arg2 == "none" else arg2
            key = None if arg3 == "none" else arg3
            dflt = None if arg4 == "none" else arg4
            message = arg5
            create_win()
            prof.win_focus(plugin_win)
            prof.cons_show_themed(group, key, dflt, message)
            prof.win_show(plugin_win, "called -> prof.cons_show_themed: " + arg2 + ", " + arg3 + ", " + arg4 + ", " + arg5)
    elif arg1 == "constest":
        res = prof.current_win_is_console()
        create_win()
        prof.win_focus(plugin_win)
        if res:
            prof.win_show(plugin_win, "called -> prof.current_win_is_console: true")
        else:
            prof.win_show(plugin_win, "called -> prof.current_win_is_console: false")
    elif arg1 == "winshow":
        if arg2 != None:
            create_win()
            prof.win_focus(plugin_win)
            prof.win_show(plugin_win, arg2)
            prof.win_show(plugin_win, "called -> prof.win_show: " + arg2)
        else:
            prof.cons_bad_cmd_usage("/python-test")
    elif arg1 == "winshow_t":
        if arg2 == None or arg3 == None or arg4 == None or arg5 == None:
            prof.cons_bad_cmd_usage("/python-test");
        else:
            group = None if arg2 == "none" else arg2
            key = None if arg3 == "none" else arg3
            dflt = None if arg4 == "none" else arg4
            message = arg5
            create_win()
            prof.win_focus(plugin_win)
            prof.win_show_themed(plugin_win, group, key, dflt, message)
            prof.win_show(plugin_win, "called -> prof_win_show_themed: " + arg2 + ", " + arg3 + ", " + arg4 + ", " + arg5)
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
            prof.win_show(plugin_win, "called -> prof.notify: " + arg2)
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
            prof.cons_bad_cmd_usage("/python-test")
    elif arg1 == "count":
        create_win()
        prof.win_focus(plugin_win)
        prof.win_show(plugin_win, "Count: " + str(count))
    elif arg1 == "ping":
        if arg2 == None:
            prof.cons_bad_cmd_usage("/python-test")
        else:
            create_win()
            prof.win_focus(plugin_win)
            res = prof.send_stanza("<iq to='" + arg2 + "' id='pythonplugin-" + str(ping_id) + "' type='get'><ping xmlns='urn:xmpp:ping'/></iq>")
            ping_id = ping_id + 1
            if res:
                prof.win_show(plugin_win, "Ping sent successfully")
            else:
                prof.win_show(plugin_win, "Error sending ping")
    else:
        prof.cons_bad_cmd_usage("/python-test")

def timed_callback():
    create_win()
    prof.win_show(plugin_win, "timed -> timed_callback called")

def prof_init(version, status):
    t = threading.Thread(target=_inc_counter)
    t.daemon = True
    t.start()

    prof.win_create(plugin_win, _handle_win_input)

    synopsis = [
        "/python-test consalert",
        "/python-test consshow <message>",
        "/python-test consshow_t <group> <key> <default> <message>",
        "/python-test constest",
        "/python-test winshow <message>",
        "/python-test winshow_t <group> <key> <default> <message>",
        "/python-test notify <message>",
        "/python-test sendline <line>",
        "/python-test get recipient|room",
        "/python-test log debug|info|warning|error <message>",
        "/python-test count",
        "/python-test ping <jid>"
    ]
    description = "Python test plugins. All commands focus the plugin window."
    args = [
        [ "consalert",                                      "Highlight the console window in the status bar" ],
        [ "consshow <message>",                             "Show the message in the console window" ],
        [ "consshow_t <group> <key> <default> <message>",   "Show the themed message in the console window. " ],
        [ "constest",                                       "Show whether the command was run in the console." ],
        [ "winshow <message>",                              "Show the message in the plugin window" ],
        [ "winshow_t <group> <key> <default> <message>",    "Show the themed message in the plugin window. " ],
        [ "notify <message>",                               "Send a desktop notification with message" ],
        [ "sendline <line>",                                "Pass line to profanity to process" ],
        [ "get recipient",                                  "Show the current chat recipient, if in a chat window" ],
        [ "get room",                                       "Show the current room JID, if ina a chat room"],
        [ "log debug|info|warning|error <message>",         "Log a message at the specified level" ],
        [ "count",                                          "Show the counter, incremented every 5 seconds by a worker thread" ],
        [ "ping <jid>",                                     "Send an XMPP ping to the specified Jabber ID" ]
    ]
    examples = [
        "/python-test sendline /about",
        "/python-test log debug \"Test debug message\"",
        "/python-test consshow_t c-test cons.show none \"This is themed\"",
        "/python-test consshow_t none none bold_cyan \"This is bold_cyan\"",
        "/python-test ping buddy@server.org"
    ]

    prof.register_command("/python-test", 1, 5, synopsis, description, args, examples, cmd_pythontest)

    prof.register_ac("/python-test", 
        [ "consalert", "consshow", "consshow_t", "constest", "winshow", "winshow_t", "notify", "sendline", "get", "log", "count", "ping" ]
    )
    prof.register_ac("/python-test get",
        [ "recipient", "room" ]
    )
    prof.register_ac("/python-test log",
        [ "debug", "info", "warning", "error" ]
    )

    prof.register_timed(timed_callback, 30)

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

