import prof

_win_tag = "Python Plugin";

def _timer_test():
    prof.cons_show("python-test: timer fired.")
    prof.cons_alert()

def _handle_upper(win, line):
    upper = line.upper();
    prof.win_show(win, upper)
    prof.win_show_red(win, upper + " red");
    prof.win_show_yellow(win, upper + " yellow")
    prof.win_show_green(win, upper + " green")
    prof.win_show_cyan(win, upper + " cyan")

def _cmd_python(msg):
    if msg:
        prof.cons_show("python-test: /python command called, arg = " + msg)
    else:
        prof.cons_show("python-test: /python command called with no arg")

def _cmd_ac(arg1=None, arg2=None):
    prof.cons_show("python-test: /py_complete called");

def _cmd_upper(line):
    global _win_tag;
    if prof.win_exists(_win_tag) == False:
        prof.win_create(_win_tag, _handle_upper)

    prof.win_focus(_win_tag)

    if line:
        _handle_upper(_win_tag, line)

def _cmd_notify():
    prof.notify("python-test: notify", 2000, "Plugins")

def _cmd_vercheck():
    prof.send_line("/vercheck")
    prof.cons_show("python-test: sent \"/vercheck\" command")

def prof_init(version, status):
    prof.cons_show("python-test: init, " + version + ", " + status)

    prof.register_command("/python", 0, 1, "/python [arg]", "python-test", "python-test", _cmd_python)

    prof.register_command("/py_upper", 1, 1, "/py_upper string", "python-test", "python-test", _cmd_upper)

    prof.register_command("/py_notify", 0, 0, "/py_notify", "python-test", "python-test", _cmd_notify)

    prof.register_command("/py_vercheck", 0, 0, "/py_vercheck", "python-test", "python-test", _cmd_vercheck)

    prof.register_ac("/py_complete", [ "aaaa", "bbbb", "bcbcbc" ])
    prof.register_ac("/py_complete aaaa", [ "one", "two", "three", "four" ])
    prof.register_ac("/py_complete bcbcbc", [ "james", "jim", "jane", "bob" ])
    prof.register_command("/py_complete", 0, 2, "/py_complete [arg1] [arg2]", "python-test", "python-test", _cmd_ac)

    prof.register_timed(_timer_test, 30)

def prof_on_start():
    prof.cons_show("python-test: prof_on_start")
    prof.log_debug("python-test: logged debug")
    prof.log_info("python-test: logged info")
    prof.log_warning("python-test: logged warning")
    prof.log_error("python-test: logged error")

def prof_on_shutdown():
    prof.log_info("python-test: prof_on_shutdown")

def prof_on_connect(account_name, fulljid):
    prof.cons_show("python-test: prof_on_connect, " + account_name + ", " + fulljid)

def prof_on_disconnect(account_name, fulljid):
    prof.cons_show("python-test: prof_on_disconnect, " + account_name + ", " + fulljid)

def prof_pre_chat_message_display(jid, message):
    prof.cons_show("python-test: prof_pre_chat_message_display, " + jid + ", " + message)
    prof.cons_alert()
    return message + "[PY_pre_chat_message_display]"

def prof_post_chat_message_display(jid, message):
    prof.cons_show("python-test: prof_post_chat_message_display, " + jid + ", " + message)
    prof.cons_alert()

def prof_pre_chat_message_send(jid, message):
    prof.cons_show("python-test: prof_pre_chat_message_send, " + jid + ", " + message)
    prof.cons_alert()
    return message + "[PY_pre_chat_message_send]"

def prof_post_chat_message_send(jid, message):
    prof.cons_show("python-test: prof_post_chat_message_send, " + jid + ", " + message)
    prof.cons_alert()

def prof_pre_room_message_display(room, nick, message):
    prof.cons_show("python-test: prof_pre_room_message_display, " + room + ", " + nick + ", " + message)
    prof.cons_alert()
    return message + "[PY_pre_room_message_display]"

def prof_post_room_message_display(room, nick, message):
    prof.cons_show("python-test: prof_post_room_message_display, " + room + ", " + nick + ", " + message)
    prof.cons_alert()

def prof_pre_room_message_send(room, message):
    prof.cons_show("python-test: prof_pre_room_message_send, " + room + ", " + message)
    prof.cons_alert()
    return message + "[PY_pre_room_message_send]"

def prof_post_room_message_send(room, message):
    prof.cons_show("python-test: prof_post_room_message_send, " + room + ", " + message)
    prof.cons_alert()

def prof_pre_priv_message_display(room, nick, message):
    prof.cons_show("python-test: prof_pre_priv_message_display, " + room + ", " + nick + ", " + message)
    prof.cons_alert()
    return message + "[PY_pre_priv_message_display]"

def prof_post_priv_message_display(room, nick, message):
    prof.cons_show("python-test: prof_post_priv_message_display, " + room + ", " + nick + ", " + message)
    prof.cons_alert()

def prof_pre_priv_message_send(room, nick, message):
    prof.cons_show("python-test: prof_pre_priv_message_send, " + room + ", " + nick + ", " + message)
    prof.cons_alert()
    return message + "[PY_pre_priv_message_send]"

def prof_post_priv_message_send(room, nick, message):
    prof.cons_show("python-test: prof_post_priv_message_send, " + room + ", " + nick + ", " + message)
    prof.cons_alert()