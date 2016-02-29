import prof
import subprocess

system_win = "System"

def _handle_win_input(win, command):
    prof.win_show_themed(win, "system", "command", None, command)
    prof.win_show(win, "")
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
    split = result.splitlines()
    for s in split:
        prof.win_show_themed(win, "system", "result", None, s)
    prof.win_show(win, "")

def create_win():
    if prof.win_exists(system_win) == False:
        prof.win_create(system_win, _handle_win_input)

def _cmd_system(command=None):
    create_win()
    prof.win_focus(system_win)
    if command:
        _handle_win_input(system_win, command)

def prof_init(version, status):
    synopsis = [
        "/system",
        "/system <command>"
    ]
    description = "Run a system command, calling with no arguments will open or focus the system window."
    args = [
        [ "<command>", "The system command to run" ]
    ]
    examples = [
        "/system \"ls -l\""
    ]
    prof.register_command("/system", 0, 1, synopsis, description, args, examples, _cmd_system)
