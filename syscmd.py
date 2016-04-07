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

def _cmd_system(arg1=None, arg2=None):
    if not arg1:
        create_win()
        prof.win_focus(system_win)
    elif arg1 == "send":
        if arg2 == None:
            prof.cons_bad_cmd_usage("/system")
        else:
            room = prof.get_current_muc()
            recipient = prof.get_current_recipient()
            if room == None and recipient == None:
                prof.cons_show("You must be in a chat or muc window to send a system command")
                prof.cons_alert()
            else:
                result = _get_result(arg2)
                prof.send_line(u'\u000A' + result)
    elif arg1 == "exec":
        if arg2 == None:
            prof.cons_bad_cmd_usage("/system")
        else:
            create_win()
            prof.win_focus(system_win)
            _handle_win_input(system_win, arg2)
    else:
        prof.cons_bad_cmd_usage("/system")

def prof_init(version, status):
    synopsis = [
        "/system",
        "/system exec <comman>",
        "/system send <command>"
    ]
    description = "Run a system command, calling with no arguments will open or focus the system window."
    args = [
        [ "exec <command>", "Execute a command" ],
        [ "send <command>", "Send the result of the command to the current recipient or room" ]
    ]
    examples = [
        "/system exec ls -l",
        "/system send uname -a"
    ]
    prof.register_command("/system", 0, 2, synopsis, description, args, examples, _cmd_system)
    prof.completer_add("/system", [ "exec", "send" ])
