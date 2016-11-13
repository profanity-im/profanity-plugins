"""
Paste the contents of the clipboard when in a chat or room window.

Dependencies:
pip install future
sudo apt-get python-tk (or python3-tk)
"""

import prof
import tkinter as tk


def _cmd_paste(arg1=None, arg2=None):
    if not arg1:
        root = tk.Tk(baseName="")
        root.withdraw()
        result = root.clipboard_get()
        newline = prof.settings_boolean_get("paste", "newline", True)
        if len(result.splitlines()) > 1 and newline:
            prof.send_line(u'\u000A' + result)
        else:
            prof.send_line(result)

        return

    if arg1 == "newline":
        if not arg2:
            prof.cons_show("")
            newline = prof.settings_boolean_get("paste", "newline", True)
            if newline:
                prof.cons_show("paste.py newline: on")
            else:
                prof.cons_show("paste.py newline: off")
        elif arg2 == "on":
            prof.settings_boolean_set("paste", "newline", True)
            prof.cons_show("paste.py newline enabled.")
        elif arg2 == "off":
            prof.settings_boolean_set("paste", "newline", False)
            prof.cons_show("paste.py newline disabled.")
        else:
            prof.cons_bad_cmd_usage("/paste")

        return

    prof.cons_bad_cmd_usage("/paste")


def prof_init(version, status, account_name, fulljid):
    synopsis = [
        "/paste",
        "/paste newline on|off"
    ]
    description = "Paste contents of clipboard."
    args = [
        [ "newline on|off", "Send newline before multiline clipboard text, defaults to on" ]
    ]
    examples = []
    prof.register_command("/paste", 0, 2, synopsis, description, args, examples, _cmd_paste)
    prof.completer_add("/paste", [ "newline" ])
    prof.completer_add("/paste newline", [ "on", "off" ])
