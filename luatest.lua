local luatest = {}

local function cmd_lua(msg)
    if msg then
        prof_cons_show("luatest: /lua command called, arg = " .. msg)
    else
        prof_cons_show("luatest: /lua command called with no arg")
    end
    prof_cons_alert()
    prof_notify("luatest: notify", 8000, "Plugins")
    prof_send_line("/account list")
    prof_cons_show("luatest: sent \"/account list\" command")
end

local function timer_test()
    prof_cons_show("luatest: timer fired.")
    recipient = prof_get_current_recipient()
    if recipient then
        prof_cons_show("  current recipient = " .. recipient)
    end
    prof_cons_alert()
end

local function handle_bracket(win, line)
    prof_win_show(win, "(" .. line .. ")")
    prof_win_show_red(win, "Red")
    prof_win_show_yellow(win, "Yellow")
    prof_win_show_green(win, "Green")
    prof_win_show_cyan(win, "Cyan")
end

local function cmd_bracket(line)
    win_tag = "Parenthesise echo";
    if prof_win_exists(win_tag) == false then
        prof_win_create(win_tag, handle_bracket);
    end

    prof_win_focus(win_tag);

    if line then
        handle_bracket(win_tag, line)
    end
end

function luatest.prof_init(version, status)
    prof_cons_show("luatest: init, " .. version .. ", " .. status)
    prof_register_command("/lua", 0, 1, "/lua", "luatest", "luatest", cmd_lua)
    prof_register_command("/bracket", 0, 1, "/bracket", "Parenthesise input string", "Parenthesise input string", cmd_bracket);
    prof_register_timed(timer_test, 10)
end

function luatest.prof_on_start()
    prof_cons_show("luatest: on_start")
    prof_log_debug("luatest: logged debug");
    prof_log_info("luatest: logged info");
    prof_log_warning("luatest: logged warning");
    prof_log_error("luatest: logged error");
end

function luatest.prof_on_connect(account_name, fulljid)
    prof_cons_show("luatest: on_connect, " .. account_name .. ", " .. fulljid)
end

function luatest.prof_on_disconnect(account_name, fulljid)
    prof_cons_show("luatest: on_disconnect, " .. account_name .. ", " .. fulljid)
    prof_log_info("luatest: on_disconnect, " .. account_name .. ", " .. fulljid)
end

function luatest.prof_on_message_received(jid, message)
    prof_cons_show("luatest: on_message_received, " .. jid .. ", " .. message)
    prof_cons_alert()
    return message .. "[LUA]"
end

function luatest.prof_on_room_message_received(room, nick, message)
    prof_cons_show("luatest: on_room_message_received, " .. room .. ", " .. nick .. ", " .. message)
    prof_cons_alert()
    return message .. "[LUA]"
end

function luatest.prof_on_private_message_received(room, nick, message)
    prof_cons_show("luatest: on_private_message_received, " .. room .. ", " .. nick .. ", " .. message)
    prof_cons_alert()
    return message .. "[LUA]"
end

function luatest.prof_on_message_send(jid, message)
    prof_cons_show("luatest: on_message_send, " .. jid .. ", " .. message)
    prof_cons_alert()
    return message .. "[LUA]"
end

function luatest.prof_on_private_message_send(room, nick, message)
    prof_cons_show("luatest: on_private_message_send, " .. room .. ", " .. nick .. ", " .. message)
    prof_cons_alert()
    return message .. "[LUA]"
end

function luatest.prof_on_room_message_send(room, message)
    prof_cons_show("luatest: on_room_message_send, " .. room .. ", " .. message)
    prof_cons_alert()
    return message .. "[LUA]"
end

function luatest.prof_on_shutdown()
    prof_log_info("luatest: on_shutdown")
end

return luatest
