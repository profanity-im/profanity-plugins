"""
Paste the contents of the clipboard when in a chat or room window.
"""

import prof
import sys
import Tkinter as tk

def _cmd_paste():
    root = tk.Tk(baseName="")
    root.withdraw()
    result = root.clipboard_get()
    recipient = prof.get_current_recipient()
    room = prof.get_current_muc()
    if recipient or room:
        prof.send_line(u'\u000A' + result)

def prof_init(version, status):
    synopsis = [
        "/paste"
    ]
    description = "Paste contents of clipboard."
    args = []
    examples = []
    prof.register_command("/paste", 0, 0, synopsis, description, args, examples, _cmd_paste)
