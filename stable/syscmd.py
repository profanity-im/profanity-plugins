"""
Allow running system commands in a plugin window, or send result to recipient

Theme options in ~/.local/share/profanity/plugin_themes

[system]
command=magenta
result=green
"""

import prof
import subprocess

system_win = "System"


def _get_result(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()


def _handle_win_input(win, command):
    prof.win_show_themed(win, "system", "command", None, command)
    prof.win_show(win, "")
    result = _get_result(command)
    split = result.splitlines()
    for s in split:
        prof.win_show_themed(win, "system", "result", None, s)
    prof.win_show(win, "")


def create_win():
    if prof.win_exists(system_win) == False:
        prof.win_create(system_win, _handle_win_input)


def _handle_send(command=None):
    if command == None:
        prof.cons_bad_cmd_usage("/system")
        return

    room = prof.get_current_muc()
    recipient = prof.get_current_recipient()
    if room == None and recipient == None:
        prof.cons_show("You must be in a chat or muc window to send a system command")
        prof.cons_alert()
        return

    result = _get_result(command)
    newline = prof.settings_boolean_get("system", "newline", True)
    if len(result.splitlines()) > 1 and newline:
        prof.send_line(u'\u000A' + result.decode('utf-8', errors='ignore'))
    else:
        prof.send_line(result)


def _handle_exec(command=None):
    if command == None:
        prof.cons_bad_cmd_usage("/system")
        return;

    create_win()
    prof.win_focus(system_win)
    _handle_win_input(system_win, command)


def _handle_newline(setting=None):
    if not setting:
        prof.cons_show("")
        newline = prof.settings_boolean_get("system", "newline", True)
        if newline:
            prof.cons_show("syscmd.py newline: on")
        else:
            prof.cons_show("syscmd.py newline: off")
        return

    if setting == "on":
        prof.settings_boolean_set("system", "newline", True)
        prof.cons_show("syscmd.py newline enabled.")
        return

    if setting == "off":
        prof.settings_boolean_set("system", "newline", False)
        prof.cons_show("syscmd.py newline disabled.")
        return

    prof.cons_bad_cmd_usage("/paste")


def _cmd_system(arg1=None, arg2=None):
    if not arg1:
        create_win()
        prof.win_focus(system_win)
        return;

    if arg1 == "newline":
        _handle_newline(arg2)
        return

    if arg1 == "send":
        _handle_send(arg2)
        return

    if arg1 == "exec":
        _handle_exec(arg2)
        return

    prof.cons_bad_cmd_usage("/system")


def prof_init(version, status, account_name, fulljid):
    synopsis = [
        "/system",
        "/system newline on|off",
        "/system exec <comman>",
        "/system send <command>"
    ]
    description = "Run a system command, calling with no arguments will open or focus the system window."
    args = [
        [ "newline on|off", "Send newline before multiline command output, defaults to on" ],
        [ "exec <command>", "Execute a command" ],
        [ "send <command>", "Send the result of the command to the current recipient or room" ]
    ]
    examples = [
        "/system exec ls -l",
        "/system send uname -a"
    ]
    prof.register_command("/system", 0, 2, synopsis, description, args, examples, _cmd_system)
    prof.completer_add("/system", [ "exec", "send", "newline" ])
    prof.completer_add("/system newline", [ "on", "off" ])
