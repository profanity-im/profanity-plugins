import prof


def _show_settings():
    prof.cons_show("Presence notify plugin settings:")
    mode = prof.settings_get_string("presence_notify", "mode", "all")
    prof.cons_show("Mode: {mode}".format(mode=mode))

    # all_list = prof.settings_get_string_list("presence_notify", "all")
    # if all_list and len(all_list) > 0:
    #     prof.cons_show("All:")
    #     for item in all_list:
    #         prof.cons_show("  {barejid}".format(barejid=item))

    # online_list = prof.settings_get_string_list("presence_notify", "online")
    # if online_list and len(online_list) > 0:
    #     prof.cons_show("Online/offline:")
    #     for item in online_list:
    #         prof.cons_show("  {barejid}".format(barejid=item))


def _cmd_presence_notify(arg1=None, arg2=None):
    if arg1 == "all":
        prof.settings_set_string("presence_notify", "mode", "all")
        prof.cons_show("Notifying on all presence changes")
        return

    if arg1 == "online":
        prof.settings_set_string("presence_notify", "mode", "online")
        prof.cons_show("Notifying on online/offline presence changes only")
        return

    if arg1 == "off":
        prof.settings_set_string("presence_notify", "mode", "off")
        prof.cons_show("Presence notifications disabled")
        return

    # if arg1 == "all":
    #     if not arg2:
    #         prof.cons_bad_cmd_usage("/presence_notify")
    #         return
    #     prof.settings_string_list_add("presence_notify", "all", arg2)
    #     prof.settings_string_list_remove("presence_notify", "online", arg2)
    #     prof.cons_show("Enabled all presence notifications for {barejid}".format(barejid=arg2))
    #     return

    # if arg1 == "online":
    #     if not arg2:
    #         prof.cons_bad_cmd_usage("/presence_notify")
    #         return
    #     prof.settings_string_list_add("presence_notify", "online", arg2)
    #     prof.settings_string_list_remove("presence_notify", "all", arg2)
    #     prof.cons_show("Enabled online/offline presence notifications for {barejid}".format(barejid=arg2))
    #     return

    _show_settings()

def prof_init(version, status, account_name, fulljid):
    synopsis = [ 
        "/presence_notify all|online|off",
        "/presence_notify all <barejid>",
        "/presence_notify online <barejid>"
    ]
    description = "Send a desktop notification on presence updates."
    args = [
        [ "all",                "Enable all presence notifications" ],
        [ "online",             "Enable only online/offline presence notifications" ],
        [ "off",                "Disable presence notifications" ],
        [ "all <barejid>",      "Enable all presence notifications for contact <barejid>"],
        [ "online <barejid>",   "Enable only online/offline presence notifications for contact <barejid>"]
    ]
    examples = [
        "/presence_notify on",
        "/presence_notify all bob@server.org"
    ]
    
    prof.register_command("/presence_notify", 0, 2, synopsis, description, args, examples, _cmd_presence_notify)

    prof.completer_add("/presence_notify",
        [ "all", "online", "off" ]
    )


def _do_notify(barejid, presence):
    mode = prof.settings_get_string("presence_notify", "mode", "all")
    if mode == "all":
        return True
    elif mode == "online":
        if presence == "online" or presence == "offline":
            return True
        else:
            return False
    else: # off
        return False

    # all_list = prof.settings_get_string_list("presence_notify", "all")
    # if not all_list:
    #     return True
    # elif len(all_list) == 0:
    #     return True    
    # elif barejid in settings_list:
    #     return True
    # else:
    #     return False


def prof_on_contact_presence(barejid, resource, presence, status, priority):
    if _do_notify(barejid, presence):
        message = "{barejid} is {presence}".format(barejid=barejid, presence=presence)
        if status:
            message = message + ", \"{status}\"".format(status=status)
        prof.notify(message, 5000, "Presence")
        return


def prof_on_contact_offline(barejid, resource, status):
    if _do_notify(barejid, "offline"):
        message = "{barejid} is offline".format(barejid=barejid)
        if status:
            message = message + ", \"{status}\"".format(status=status)
        prof.notify(message, 5000, "Presence")
        return