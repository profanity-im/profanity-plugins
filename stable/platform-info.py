"""
Shows platform details in the console

Theme items in ~/.local/share/profanity/plugin_themes

[platform]
line=cyan
"""

import prof
import platform


def _cmd_platform():
    result_summary = platform.platform()
    prof.cons_show_themed("platform", "line", None, result_summary)


def prof_init(version, status, account_name, fulljid):
    synopsis = [ 
        "/platform"
    ]
    description = "Output system information to the console window."
    args = []
    examples = []

    prof.register_command("/platform", 0, 0, synopsis, description, args, examples, _cmd_platform)
