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


def _create_win():
    if prof.win_exists(plugin_win) == False:
        prof.win_create(plugin_win, _handle_win_input)


def _consalert():
    _create_win()
    prof.win_focus(plugin_win)
    prof.cons_alert()
    prof.win_show(plugin_win, "called -> prof.cons_alert")


def _consshow(msg):
    if not msg:
        prof.cons_bad_cmd_usage("/python-test")
        return

    _create_win()
    prof.win_focus(plugin_win)
    prof.cons_show(msg)
    prof.win_show(plugin_win, "called -> prof.cons_show: " + msg)


def _consshow_t(group, key, dflt, msg):
    if not group or not key or not dflt or not msg:
        prof.cons_bad_cmd_usage("/python-test")
        return

    _create_win()
    prof.win_focus(plugin_win)
    groupval = None if group == "none" else group
    keyval = None if key == "none" else key
    dfltval = None if dflt == "none" else dflt
    prof.cons_show_themed(groupval, keyval, dfltval, msg)
    prof.win_show(plugin_win, "called -> prof.cons_show_themed: " + group + ", " + key + ", " + dflt + ", " + msg)


def _constest():
    res = prof.current_win_is_console()
    _create_win()
    prof.win_focus(plugin_win)
    if res:
        prof.win_show(plugin_win, "called -> prof.current_win_is_console: true")
    else:
        prof.win_show(plugin_win, "called -> prof.current_win_is_console: false")


def _winshow(msg):
    if not msg:
        prof.cons_bad_cmd_usage("/python-test")
        return

    _create_win()
    prof.win_focus(plugin_win)
    prof.win_show(plugin_win, msg)
    prof.win_show(plugin_win, "called -> prof.win_show: " + msg)


def _winshow_t(group, key, dflt, msg):
    if not group or not key or not dflt or not msg:
        prof.cons_bad_cmd_usage("/python-test")
        return

    _create_win()
    prof.win_focus(plugin_win)
    groupval = None if group == "none" else group
    keyval = None if key == "none" else key
    dfltval = None if dflt == "none" else dflt
    prof.win_show_themed(plugin_win, groupval, keyval, dfltval, msg)
    prof.win_show(plugin_win, "called -> prof_win_show_themed: " + group + ", " + key + ", " + dflt + ", " + msg)


def _sendline(line):
    if not line:
        prof.cons_bad_cmd_usage("/python-test")
        return

    _create_win()
    prof.win_focus(plugin_win)
    prof.send_line(line)
    prof.win_show(plugin_win, "called -> prof.send_line: " + line)


def _notify(msg):
    if not msg:
        prof.cons_bad_cmd_usage("/python-test")
        return

    _create_win()
    prof.win_focus(plugin_win)
    prof.notify(msg, 5000, "python-test plugin")
    prof.win_show(plugin_win, "called -> prof.notify: " + msg)


def _get(subject):
    if subject == "recipient":
        _create_win()
        recipient = prof.get_current_recipient();
        if recipient:
            prof.win_focus(plugin_win)
            prof.win_show(plugin_win, "called -> prof.get_current_recipient: " + recipient)
        else:
            prof.win_focus(plugin_win)
            prof.win_show(plugin_win, "called -> prof_get_current_recipient: <none>")
    elif subject == "room":
        _create_win()
        room = prof.get_current_muc()
        if room:
            prof.win_focus(plugin_win)
            prof.win_show(plugin_win, "called -> prof_get_current_muc: " + room)
        else:
            prof.win_focus(plugin_win)
            prof.win_show(plugin_win, "called -> prof_get_current_muc: <none>")
    elif subject == "nick":
        _create_win()
        nick = prof.get_current_nick()
        if nick:
            prof.win_focus(plugin_win)
            prof.win_show(plugin_win, "called -> prof_get_current_nick: " + nick)
        else:
            prof.win_focus(plugin_win)
            prof.win_show(plugin_win, "called -> prof_get_current_nick: <none>")
    elif subject == "occupants":
        _create_win()
        occupants = prof.get_current_occupants()
        if occupants:
            prof.win_focus(plugin_win)
            prof.win_show(plugin_win, "called -> prof_get_current_occupants:")
            for occupant in occupants:
                prof.win_show(plugin_win, occupant)
        else:
            prof.win_focus(plugin_win)
            prof.win_show(plugin_win, "called -> prof_get_current_occupants: <none>")
    else:
        prof.cons_bad_cmd_usage("/python-test")


def _log(level, msg):
    if not level or not msg:
        prof.cons_bad_cmd_usage("/python-test")
        return

    if level == "debug":
        _create_win()
        prof.win_focus(plugin_win)
        prof.log_debug(msg)
        prof.win_show(plugin_win, "called -> prof.log_debug: " + msg)
    elif level == "info":
        _create_win()
        prof.win_focus(plugin_win)
        prof.log_info(msg)
        prof.win_show(plugin_win, "called -> prof.log_info: " + msg)
    elif level == "warning":
        _create_win()
        prof.win_focus(plugin_win)
        prof.log_warning(msg)
        prof.win_show(plugin_win, "called -> prof.log_warning: " + msg)
    elif level == "error":
        _create_win()
        prof.win_focus(plugin_win)
        prof.log_error(msg)
        prof.win_show(plugin_win, "called -> prof.log_error: " + msg)
    else:
        prof.cons_bad_cmd_usage("/python-test")


def _count():
    _create_win()
    prof.win_focus(plugin_win)
    prof.win_show(plugin_win, "Count: " + str(count))


def _ping(jid):
    global ping_id

    if not jid:
        prof.cons_bad_cmd_usage("/python-test")
        return

    _create_win()
    prof.win_focus(plugin_win)
    res = prof.send_stanza("<iq to='" + jid + "' id='pythonplugin-" + str(ping_id) + "' type='get'><ping xmlns='urn:xmpp:ping'/></iq>")
    ping_id = ping_id + 1
    if res:
        prof.win_show(plugin_win, "Ping sent successfully")
    else:
        prof.win_show(plugin_win, "Error sending ping")


def _boolean(op, group, key, value_str):
    if op != "get" and op != "set":
        prof.cons_bad_cmd_usage("/python-test")
        return

    if group == None or key == None:
        prof.cons_bad_cmd_usage("/python-test")
        return

    if op == "set" and value_str != "true" and value_str != "false":
        prof.cons_bad_cmd_usage("/python-test")
        return

    if op == "get":
        dflt = False
        _create_win()
        prof.win_focus(plugin_win)
        res = prof.settings_get_boolean(group, key, dflt)
        if res:
            prof.win_show(plugin_win, "Boolean setting: TRUE")
        else:
            prof.win_show(plugin_win, "Boolean setting: FALSE")
    elif op == "set":
        value = False
        if value_str == "true":
            value = True
        _create_win()
        prof.win_focus(plugin_win)
        prof.settings_set_boolean(group, key, value)
        prof.win_show(plugin_win, "Set [" + group + "] " + key + " to " + str(value))


def _string(op, group, key, value):
    if op != "get" and op != "set":
        prof.cons_bad_cmd_usage("/python-test")
        return

    if group == None or key == None:
        prof.cons_bad_cmd_usage("/python-test")
        return

    if op == "set" and not value:
        prof.cons_bad_cmd_usage("/python-test")
        return

    if op == "get":
        _create_win()
        prof.win_focus(plugin_win)
        res = prof.settings_get_string(group, key, None)
        if res:
            prof.win_show(plugin_win, "String setting: " + res)
        else:
            prof.win_show(plugin_win, "String setting: None")
    elif op == "set":
        _create_win()
        prof.win_focus(plugin_win)
        prof.settings_set_string(group, key, value)
        prof.win_show(plugin_win, "Set [" + group + "] " + key + " to " + value)


def _int(op, group, key, value):
    if op != "get" and op != "set":
        prof.cons_bad_cmd_usage("/python-test")
        return

    if group == None or key == None:
        prof.cons_bad_cmd_usage("/python-test")
        return

    if op == "get":
        _create_win()
        prof.win_focus(plugin_win)
        res = prof.settings_get_int(group, key, 0)
        prof.win_show(plugin_win, "Integer setting: " + str(res))
    elif op == "set":
        _create_win()
        prof.win_focus(plugin_win)
        prof.settings_set_int(group, key, int(value))
        prof.win_show(plugin_win, "Set [" + group + "] " + key + " to " + str(value))


def _incoming(barejid, resource, message):
    if not barejid or not resource or not message:
        prof.cons_bad_cmd_usage("/python-test")
        return

    prof.incoming_message(barejid, resource, message)


def _completer(op, item):
    if not item:
        prof.cons_bad_cmd_usage("/python-test")
        return

    if op == "add":
        _create_win()
        prof.win_focus(plugin_win)
        prof.completer_add("/python-test", [item])
        prof.win_show(plugin_win, "Added \"" + item + "\" to /python-test completer")
        prof.completer_add("/python-test completer remove", [item])
    elif op == "remove":
        _create_win()
        prof.win_focus(plugin_win)
        prof.completer_remove("/python-test", [item])
        prof.win_show(plugin_win, "Removed \"" + item + "\" to /python-test completer")
        prof.completer_remove("/python-test completer remove", [item])
    else:
        prof.cons_bad_cmd_usage("/python-test")


def _cmd_pythontest(subcmd=None, arg1=None, arg2=None, arg3=None, arg4=None):
    if      subcmd == "consalert":  _consalert()
    elif    subcmd == "consshow":   _consshow(arg1)
    elif    subcmd == "consshow_t": _consshow_t(arg1, arg2, arg3, arg4)
    elif    subcmd == "constest":   _constest()
    elif    subcmd == "winshow":    _winshow(arg1)
    elif    subcmd == "winshow_t":  _winshow_t(arg1, arg2, arg3, arg4)
    elif    subcmd == "sendline":   _sendline(arg1)
    elif    subcmd == "notify":     _notify(arg1)
    elif    subcmd == "get":        _get(arg1)
    elif    subcmd == "log":        _log(arg1, arg2)
    elif    subcmd == "count":      _count()
    elif    subcmd == "ping":       _ping(arg1)
    elif    subcmd == "boolean":    _boolean(arg1, arg2, arg3, arg4)
    elif    subcmd == "string":     _string(arg1, arg2, arg3, arg4)
    elif    subcmd == "int":        _int(arg1, arg2, arg3, arg4)
    elif    subcmd == "incoming":   _incoming(arg1, arg2, arg3)
    elif    subcmd == "completer":  _completer(arg1, arg2)
    else:                           prof.cons_bad_cmd_usage("/python-test")


def timed_callback():
    _create_win()
    prof.win_show(plugin_win, "timed -> timed_callback called")


def prof_init(version, status, account_name, fulljid):
    t = threading.Thread(target=_inc_counter)
    t.daemon = True
    t.start()

    prof.disco_add_feature("urn:xmpp:profanity:python_test_plugin");

    prof.win_create(plugin_win, _handle_win_input)
    if account_name and fulljid:
        prof.win_show(plugin_win, "fired -> prof_init: " + version + ", " + status + ", " + account_name + ", " + fulljid)
    else:
        prof.win_show(plugin_win, "fired -> prof_init: " + version + ", " + status)

    synopsis = [
        "/python-test consalert",
        "/python-test consshow <message>",
        "/python-test consshow_t <group> <key> <default> <message>",
        "/python-test constest",
        "/python-test winshow <message>",
        "/python-test winshow_t <group> <key> <default> <message>",
        "/python-test notify <message>",
        "/python-test sendline <line>",
        "/python-test get recipient|room|nick|occupants",
        "/python-test log debug|info|warning|error <message>",
        "/python-test count",
        "/python-test ping <jid>",
        "/python-test boolean get <group> <key>",
        "/python-test boolean set <group> <key> <value>",
        "/python-test string get <group> <key>",
        "/python-test string set <group> <key> <value>",
        "/python-test int get <group> <key>",
        "/python-test int set <group> <key> <value>",
        "/python-test incoming <barejid> <resource> <message>",
        "/python-test completer add|remove <item>"
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
        [ "get nick",                                       "Show nickname in current room, if ina a chat room"],
        [ "get occupants",                                  "Show occupants in current room, if ina a chat room"],
        [ "log debug|info|warning|error <message>",         "Log a message at the specified level" ],
        [ "count",                                          "Show the counter, incremented every 5 seconds by a worker thread" ],
        [ "ping <jid>",                                     "Send an XMPP ping to the specified Jabber ID" ],
        [ "boolean get <group> <key>",                      "Get a boolean setting" ],
        [ "boolean set <group> <key> <value>",              "Set a boolean setting" ],
        [ "string get <group> <key>",                       "Get a string setting" ],
        [ "string set <group> <key> <value>",               "Set a string setting" ],
        [ "int get <group> <key>",                          "Get a integer setting" ],
        [ "int set <group> <key> <value>",                  "Set a integer setting" ],
        [ "incoming <barejid> <resource> <message>",        "Show an incoming message." ],
        [ "completer add <item>",                           "Add an autocomplete item to the /c-test command." ],
        [ "completer remove <item>",                        "Remove an autocomplete item from the /c-test command." ]
    ]
    examples = [
        "/python-test sendline /about",
        "/python-test log debug \"Test debug message\"",
        "/python-test consshow_t c-test cons.show none \"This is themed\"",
        "/python-test consshow_t none none bold_cyan \"This is bold_cyan\"",
        "/python-test ping buddy@server.org"
    ]

    prof.register_command("/python-test", 1, 5, synopsis, description, args, examples, _cmd_pythontest)

    prof.completer_add("/python-test",
        [
            "consalert",
            "consshow",
            "consshow_t",
            "constest",
            "winshow",
            "winshow_t",
            "notify",
            "sendline",
            "get",
            "log",
            "count",
            "ping",
            "boolean",
            "string",
            "int",
            "incoming",
            "completer" 
        ]
    )
    prof.completer_add("/python-test get",
        [ "recipient", "room", "nick", "occupants" ]
    )
    prof.completer_add("/python-test log",
        [ "debug", "info", "warning", "error" ]
    )
    prof.completer_add("/python-test boolean",
        [ "get", "set" ]
    )
    prof.completer_add("/python-test string",
        [ "get", "set" ]
    )
    prof.completer_add("/python-test int",
        [ "get", "set" ]
    )
    prof.completer_add("/python-test completer",
        [ "add", "remove" ]
    )

    prof.register_timed(timed_callback, 5)


def prof_on_start():
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_on_start")


def prof_on_shutdown():
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_on_shutdown")


def prof_on_unload():
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_on_unload")


def prof_on_connect(account_name, fulljid):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_on_connect: " + account_name + ", " + fulljid)


def prof_on_disconnect(account_name, fulljid):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_on_disconnect: " + account_name + ", " + fulljid)


def prof_pre_chat_message_display(jid, message):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_pre_chat_message_display: " + jid + ", " + message)


def prof_post_chat_message_display(jid, message):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_post_chat_message_display: " + jid + ", " + message)


def prof_pre_chat_message_send(jid, message):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_pre_chat_message_send: " + jid + ", " + message)


def prof_post_chat_message_send(jid, message):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_post_chat_message_send: " + jid + ", " + message)


def prof_pre_room_message_display(room, nick, message):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_pre_room_message_display: " + room + ", " + nick + ", " + message)


def prof_post_room_message_display(room, nick, message):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_post_room_message_display: " + room + ", " + nick + ", " + message)


def prof_pre_room_message_send(room, message):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_pre_room_message_send: " + room + ", " + message)


def prof_post_room_message_send(room, message):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_post_room_message_send: " + room + ", " + message)


def prof_on_room_history_message(room, nick, message, timestamp):
    _create_win()
    if timestamp:
        prof.win_show(plugin_win, "fired -> prof_on_room_history_message: " + room + ", " + nick + ", " + message + ", " + timestamp)
    else:
        prof.win_show(plugin_win, "fired -> prof_on_room_history_message: " + room + ", " + nick + ", " + message)


def prof_pre_priv_message_display(room, nick, message):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_pre_priv_message_display: " + room + ", " + nick + ", " + message)


def prof_post_priv_message_display(room, nick, message):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_post_priv_message_display: " + room + ", " + nick + ", " + message)


def prof_pre_priv_message_send(room, nick, message):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_pre_priv_message_send: " + room + ", " + nick + ", " + message)


def prof_post_priv_message_send(room, nick, message):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_post_priv_message_send: " + room + ", " + nick + ", " + message)


def prof_on_message_stanza_send(stanza):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_on_message_stanza_send: " + stanza)


def prof_on_message_stanza_receive(stanza):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_on_message_stanza_receive: " + stanza)
    return True


def prof_on_presence_stanza_send(stanza):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_on_presence_stanza_send: " + stanza)


def prof_on_presence_stanza_receive(stanza):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_on_presence_stanza_receive: " + stanza)
    return True


def prof_on_iq_stanza_send(stanza):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_on_iq_stanza_send: " + stanza)


def prof_on_iq_stanza_receive(stanza):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_on_iq_stanza_receive: " + stanza)
    return True


def prof_on_contact_offline(barejid, resource, status):
    _create_win()
    if status:
        prof.win_show(plugin_win, "fired -> prof_on_contact_offline: " + barejid + "/" + resource + " \"" + status + "\"")
    else:
        prof.win_show(plugin_win, "fired -> prof_on_contact_offline: " + barejid + "/" + resource)


def prof_on_contact_presence(barejid, resource, presence, status, priority):
    _create_win()
    if status:
        prof.win_show(plugin_win, "fired -> prof_on_contact_presence: " + barejid + "/" + resource + " " + presence + " " + str(priority) + " \"" + status + "\"")
    else:
        prof.win_show(plugin_win, "fired -> prof_on_contact_presence: " + barejid + "/" + resource + " " + presence + " " + str(priority))


def prof_on_chat_win_focus(barejid):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_on_chat_win_focus: " + barejid)


def prof_on_room_win_focus(roomjid):
    _create_win()
    prof.win_show(plugin_win, "fired -> prof_on_room_win_focus: " + roomjid)
