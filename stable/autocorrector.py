"""
autocorrector - Replace common typos
My typing style is such a mess. But I invest more time in correcting it
programmatically than training myself to type better. Maybe thats the
problem? Anyway, here is a plugin for all keyboard messies like me.
"""
import prof

def prof_pre_chat_message_send(barejid, message):
    enabled = prof.settings_string_get("autocorrector", "enabled", "on")
    if enabled == "off":
        return message
    else:
        replacements = prof.settings_string_list_get("autocorrector","replacements")
        for replacement in replacements:
            repl=replacement.split(':')
            message=message.replace(repl[0],repl[1])
        return message

def prof_pre_priv_message_send(barejid, nick, message):
    enabled = prof.settings_string_get("autocorrector", "enabled", "on")
    if enabled == "off":
        return message
    else:
        replacements = prof.settings_string_list_get("autocorrector","replacements")
        for replacement in replacements:
            repl=replacement.split(':')
            message=message.replace(repl[0],repl[1])
        return message

def prof_pre_room_message_send(barejid, message):
    enabled = prof.settings_string_get("autocorrector", "enabled", "on")
    if enabled == "off":
        return message
    else:
        replacements = prof.settings_string_list_get("autocorrector","replacements")
        for replacement in replacements:
            repl=replacement.split(':')
            message=message.replace(repl[0],repl[1])
        return message

def _cmd_autocorrector(arg1=None, arg2=None):
    if arg1 == "on":
        prof.settings_string_set("autocorrector", "enabled", "on")
        prof.cons_show("autocorrector plugin enabled")
    elif arg1 == "off":
        prof.settings_string_set("autocorrector", "enabled", "off")
        prof.cons_show("autocorrector plugin disabled")
    elif arg1 == "clearall":
        prof.settings_string_list_clear("autocorrector","replacements")
        prof.cons_show("autocorrector plugin replacement list cleared.")
    elif arg1 == "showlist":
        replacements = prof.settings_string_list_get("autocorrector","replacements")
        prof.cons_show("Replacement string list:")
        for replacement in replacements:
            prof.cons_show(replacement)
    elif arg1 == "add":
        if arg2 == None:
            prof.cons_bad_cmd_usage("/autocorrector")
        else:
            if len(arg2.split(':')) == 2:
                prof.settings_string_list_add("autocorrector","replacements",arg2)
                prof.cons_show("Replacement String added.")
            else:
                prof.cons_show("Invalid replacement String. Please use the following format to specify replacements: pattern:replacement.")
    elif arg1 == "rm":
        if arg2 == None:
            prof.cons_bad_cmd_usage("/autocorrector")
        else:
            if len(arg2.split(':')) == 2:
                prof.settings_string_list_remove("autocorrector","replacements",arg2)
                prof.cons_show("Replacement String removed.")
            else:
                prof.cons_show("Invalid replacement String. Please use the following format to specify replacements: pattern:replacement.")
    else:
        enabled = prof.settings_string_get("autocorrector", "enabled", "on")
        if enabled == "off":
            prof.cons_show("autocorrector inactive.")
        else:
            prof.cons_show("autocorrector active.")

def prof_init(version, status, account_name, fulljid):
    synopsis = [
        "/autocorrector on|off",
        "/autocorrector showlist",
        "/autocorrector clearall",
        "/autocorrector add"
        "/autocorrector rm"
    ]
    description = "Messy typist autocorrector. Replaces common typos in your outgoing messages."
    args = [
        [ "on|off",         "Enable/disable correction for all windows" ],
        [ "showlist",       "show typolist." ],
        [ "add",            "Add entry to typolist. Use pattern:replacement as format." ],
        [ "rm",             "Remove entry from typolist. Use pattern:replacement as format." ],
        [ "clearall",       "Remove all entries from typolist" ]
    ]
    examples = [
        "/autocorrector on",
        "/autocorrector add tpyo:typo",
        "/autocorrector add tset:test",
        "/autocorrector rm tset:test",
        "/autocorrector showlist",
    ]

    prof.settings_string_set("autocorrector", "enabled", "on")
    prof.register_command("/autocorrector", 0, 2, synopsis, description, args, examples, _cmd_autocorrector)
    prof.completer_add("/autocorrector", [ "on", "off", "clearall", "add", "rm", "showlist" ])

