import prof

_win_tag = "Upper echo";

def _cmd_python(msg):
    if msg:
        prof.cons_show("python-test: /python command called, arg = " + msg)
    else:
        prof.cons_show("python-test: /python command called with no arg")
    prof.cons_alert()
    prof.notify("python-test: notify", 2000, "Plugins")
    prof.send_line("/vercheck")
    prof.cons_show("python-test: sent \"/vercheck\" command")

def _timer_test():
    prof.cons_show("python-test: timer fired.")
    recipient = prof.get_current_recipient()
    if recipient:
        prof.cons_show("  current recipient = " + recipient)
    prof.cons_alert()

def _cmd_upper(line):
    global _win_tag;
    if prof.win_exists(_win_tag) == False:
        prof.win_create(_win_tag, _handle_upper)

    prof.win_focus(_win_tag)

    if line:
        prof.win_process_line(_win_tag, line)

def _handle_upper(win, line):
    prof.win_show(win, line.upper())

def prof_init(version, status):
    prof.cons_show("python-test: init, " + version + ", " + status)
    prof.register_command("/python", 0, 1, "/python", "python-test", "python-test", _cmd_python)
    prof.register_command("/upper", 0, 1, "/upper", "Uppercase input string", "Uppercase input string", _cmd_upper)
    prof.register_timed(_timer_test, 10)

def prof_on_start():
    prof.cons_show("python-test: on_start")
    prof.log_debug("python-test: logged debug")
    prof.log_info("python-test: logged info")
    prof.log_warning("python-test: logged warning")
    prof.log_error("python-test: logged error")

def prof_on_connect(account_name, fulljid):
    prof.cons_show("python-test: on_connect, " + account_name + ", " + fulljid)

def prof_on_disconnect(account_name, fulljid):
    prof.cons_show("python-test: on_disconnect, " + account_name + ", " + fulljid)
    prof.log_info("python-test: on_disconnect, " + account_name + ", " + fulljid)

def prof_on_message_received(jid, message):
    prof.cons_show("python-test: on_message_received, " + jid + ", " + message)
    prof.cons_alert()
    return message + "[PYTHON]"

def prof_on_room_message_received(room, nick, message):
    prof.cons_show("python-test: on_room_message_received, " + room + ", " + nick + ", " + message)
    prof.cons_alert()
    return message + "[PYTHON]"

def prof_on_private_message_received(room, nick, message):
    prof.cons_show("python-test: on_private_message_received, " + room + ", " + nick + ", " + message)
    prof.cons_alert()
    return message + "[PYTHON]"

def prof_on_message_send(jid, message):
    prof.cons_show("python-test: on_message_send, " + jid + ", " + message)
    prof.cons_alert()
    return message + "[PYTHON]"

def prof_on_private_message_send(room, nick, message):
    prof.cons_show("python-test: on_private_message_send, " + room + ", " + nick + ", " + message)
    prof.cons_alert()
    return message + "[PYTHON]"

def prof_on_room_message_send(room, message):
    prof.cons_show("python-test: on_room_message_send, " + room + ", " + message)
    prof.cons_alert()
    return message + "[PYTHON]"

def prof_on_shutdown():
    prof.log_info("python-test: on_shutdown")
