import prof


def _show_settings():
    prof.cons_show("Presence notify plugin settings:")
    mode = prof.settings_get_string("presence_notify", "mode", "all")
    prof.cons_show("Mode: {mode}".format(mode=mode))

    ignored_list = prof.settings_get_string_list("presence_notify", "ignored")
    if ignored_list and len(ignored_list) > 0:
        prof.cons_show("Ignored:")
        for contact in ignored_list:
            prof.cons_show("  {barejid}".format(barejid=contact))


def _cmd_presence_notify(arg1=None, arg2=None, arg3=None):
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

    if arg1 == "ignored":
        if arg2 == "clear":
            prof.settings_string_list_remove_all("presence_notify", "ignored")
            prof.cons_show("Removed all ignored contacts for presence notifications")
            return

        if arg2 == "add":
            if not arg3:
                prof.cons_bad_cmd_usage("/presence_notify")
                return
            prof.settings_string_list_add("presence_notify", "ignored", arg3)
            prof.cons_show("Added {contact} to ignored contacts for presence notifications".format(contact=arg3))
            return

        if arg2 == "remove":
            if not arg3:
                prof.cons_bad_cmd_usage("/presence_notify")
                return
            res = prof.settings_string_list_remove("presence_notify", "ignored", arg3)
            if res:
                prof.cons_show("Removed {contact} from ignored contacts for presence notifications".format(contact=arg3))
            else:
                prof.cons_show("{contact} not in ignore list for presence notiications".format(contact=arg3))
            return

        prof.cons_bad_cmd_usage("/presence_notify")
        return

    _show_settings()


def prof_init(version, status, account_name, fulljid):
    synopsis = [ 
        "/presence_notify all|online|off",
        "/presence_notify ignored add|remove|clear [<barejid>]"
    ]
    description = "Send a desktop notification on presence updates."
    args = [
        [ "all",                            "Enable all presence notifications" ],
        [ "online",                         "Enable only online/offline presence notifications" ],
        [ "off",                            "Disable presence notifications" ],
        [ "ignored add|remove <barejid>",   "Add or remove a contact from the list excluded from presence notifications"],
        [ "ignored clear",                  "Clear the list of excluded contacts"]
    ]
    examples = [
        "/presence_notify all",
        "/presence_notify ignored add bob@server.org"
    ]

    prof.register_command("/presence_notify", 0, 3, synopsis, description, args, examples, _cmd_presence_notify)

    prof.completer_add("/presence_notify",
        [ "all", "online", "off", "ignored" ]
    )
    prof.completer_add("/presence_notify ignored",
        [ "add", "remove", "clear" ]
    )


def _do_notify(barejid, presence):
    ignored = prof.settings_get_string_list("presence_notify", "ignored")
    if ignored and barejid in ignored:
        return False

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