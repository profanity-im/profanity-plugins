import prof


def _cmd_presence_notify(arg1=None, arg2=None):
    if arg1 == "on":
        prof.settings_set_boolean("presence_notify", "enabled", True)
        prof.cons_show("Presence notifications enabled")
        return

    if arg1 == "off":
        prof.settings_set_boolean("presence_notify", "enabled", False)
        prof.cons_show("Presence notifications disabled")
        return

    if arg1 == "all":
        if not arg2:
            prof.cons_bad_cmd_usage("/presence_notify")
            return
        prof.settings_string_list_add("presence_notify", "all", arg2)
        prof.settings_string_list_remove("presence_notify", "online", arg2)
        prof.cons_show("Enabled all presence notifications for {barejid}".format(barejid=arg2))
        return

    prof.cons_show("Presence notify plugin settings:")
    enabled = prof.settings_get_boolean("presence_notify", "enabled", False)
    if enabled:
        prof.cons_show("Enabled: ON")
    else:
        prof.cons_show("Enabled: OFF")
    all_res = prof.settings_get_string_list("presence_notify", "all")
    if all_res and len(all_res) > 0:
        prof.cons_show("All:")
        for item in all_res:
            prof.cons_show("  {barejid}".format(barejid=item))


def prof_init(version, status, account_name, fulljid):
    synopsis = [ 
        "/presence_notify on|off",
        "/presence_notify all <barejid>" 
    ]
    description = "Send a desktop notification on presence updates."
    args = [
        [ "on|off",         "Enable/disable presence notifications" ],
        [ "all <barejid>",  "Enable all presence notifications for contact <barejid>"]
    ]
    examples = [
        "/presence_notify on",
        "/presence_notify all bob@server.org"
    ]
    
    prof.register_command("/presence_notify", 0, 2, synopsis, description, args, examples, _cmd_presence_notify)

    prof.completer_add("/presence_notify",
        [ "on", "off", "all" ]
    )


def prof_on_contact_presence(barejid, resource, presence, status, priority):
    enabled = prof.settings_get_boolean("presence_notify", "enabled", False)
    if enabled:
        all_res = prof.settings_get_string_list("presence_notify", "all")
        if not all_res or len(all_res) == 0:
            prof.notify("{barejid} is {presence}".format(barejid=barejid, presence=presence), 5000, "Presence")
        elif barejid in all_res:
            prof.notify("{barejid} is {presence}".format(barejid=barejid, presence=presence), 5000, "Presence")


def prof_on_contact_offline(barejid, resource, status):
    enabled = prof.settings_get_boolean("presence_notify", "enabled", False)
    if enabled:
        all_res = prof.settings_get_string_list("presence_notify", "all")
        if not all_res or len(all_res) == 0:
            prof.notify("{barejid} is offline".format(barejid=barejid), 5000, "Presence")
        elif barejid in all_res:
            prof.notify("{barejid} is offline".format(barejid=barejid), 5000, "Presence")
