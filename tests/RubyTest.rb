module RubyTest

    def self.prof_init(version, status)
        Prof::cons_show("RubyTest: init, " + version + ", " + status)
        Prof::register_command("/ruby", 0, 1, "/ruby [arg]", "RubyTest", "RubyTest", cmd_ruby)
        Prof::register_command("/rb_upper", 1, 1, "/rb_upper string", "RubyTest", "RubyTest", cmd_upper)
        Prof::register_command("/rb_notify", 0, 0, "/rb_notify", "RubyTest", "RubyTest", cmd_notify)
        Prof::register_command("/rb_vercheck", 0, 0, "/rb_vercheck", "RubyTest", "RubyTest", cmd_vercheck)
        Prof::register_ac("/rb_complete", [ "aaaa", "bbbb", "bcbcbc" ])
        Prof::register_ac("/rb_complete aaaa", [ "one", "two", "three", "four" ])
        Prof::register_ac("/rb_complete bcbcbc", [ "james", "jim", "jane", "bob" ])
        Prof::register_command("/rb_complete", 0, 2, "/rb_complete [arg1] [arg2]", "RubyTest", "RubyTest", cmd_ac)
        Prof::register_timed(timer_test, 30)
    end

    def self.prof_on_start
        Prof::cons_show("RubyTest: prof_on_start")
        Prof::log_debug("RubyTest: logged debug");
        Prof::log_info("RubyTest: logged info");
        Prof::log_warning("RubyTest: logged warning");
        Prof::log_error("RubyTest: logged error");
    end

    def self.prof_on_shutdown
        Prof::log_info("RubyTest: prof_on_shutdown");
    end

    def self.prof_on_connect(account_name, fulljid)
        Prof::cons_show("RubyTest: prof_on_connect, " + account_name + ", " + fulljid)
    end

    def self.prof_on_disconnect(account_name, fulljid)
        Prof::cons_show("RubyTest: prof_on_disconnect, " + account_name + ", " + fulljid)
    end

    def self.prof_pre_chat_message_display(jid, message)
        Prof::cons_show("RubyTest: prof_pre_chat_message_display, " + jid + ", " + message)
        Prof::cons_alert
        return message + "[RB_pre_chat_message_display]"
    end

    def self.prof_post_chat_message_display(jid, message)
        Prof::cons_show("RubyTest: prof_post_chat_message_display, " + jid + ", " + message)
        Prof::cons_alert
    end

    def self.prof_pre_chat_message_send(jid, message)
        Prof::cons_show("RubyTest: prof_pre_chat_message_send, " + jid + ", " + message)
        Prof::cons_alert
        return message + "[RB_pre_chat_message_send]"
    end

    def self.prof_post_chat_message_send(jid, message)
        Prof::cons_show("RubyTest: prof_post_chat_message_send, " + jid + ", " + message)
        Prof::cons_alert
    end

    def self.prof_pre_room_message_display(room, nick, message)
        Prof::cons_show("RubyTest: prof_pre_room_message_display, " + room + ", " + nick + ", " + message)
        Prof::cons_alert
        return message + "[RB_pre_room_message_display]"
    end

    def self.prof_post_room_message_display(room, nick, message)
        Prof::cons_show("RubyTest: prof_post_room_message_display, " + room + ", " + nick + ", " + message)
        Prof::cons_alert
    end

    def self.prof_pre_room_message_send(room, message)
        Prof::cons_show("RubyTest: prof_pre_room_message_send, " + room + ", " + message)
        Prof::cons_alert
        return message + "[RB_pre_room_message_send]"
    end

    def self.prof_post_room_message_send(room, message)
        Prof::cons_show("RubyTest: prof_post_room_message_send, " + room + ", " + message)
        Prof::cons_alert
    end

    def self.prof_pre_priv_message_display(room, nick, message)
        Prof::cons_show("RubyTest: prof_pre_priv_message_display, " + room + ", " + nick + ", " + message)
        Prof::cons_alert
        return message + "[RB_pre_priv_message_display]"
    end

    def self.prof_post_priv_message_display(room, nick, message)
        Prof::cons_show("RubyTest: prof_post_priv_message_display, " + room + ", " + nick + ", " + message)
        Prof::cons_alert
    end

    def self.prof_pre_priv_message_send(room, nick, message)
        Prof::cons_show("RubyTest: prof_pre_priv_message_send, " + room + ", " + nick + ", " + message)
        Prof::cons_alert
        return message + "[RB_pre_priv_message_send]"
    end

    def self.prof_post_priv_message_send(room, nick, message)
        Prof::cons_show("RubyTest: prof_post_priv_message_send, " + room + ", " + nick + ", " + message)
        Prof::cons_alert
    end

    def self.cmd_ruby
        return Proc.new { | msg |
            if msg
                Prof::cons_show("RubyTest: /ruby command called, arg = " + msg)
            else
                Prof::cons_show("RubyTest: /ruby command called with no arg")
            end
        }
    end

    def self.cmd_ac
        return Proc.new { | arg1, arg2 |
            Prof::cons_show("RubyTest: /rb_complete called")
        }
    end

    def self.cmd_notify
        return Proc.new {
            Prof::notify("RubyTest: notify", 2000, "Plugins")
        }
    end

    def self.cmd_vercheck
        return Proc.new {
            Prof::send_line("/vercheck")
            Prof::cons_show("RubyTest: sent \"/vercheck\" command")
        }
    end

    def self.timer_test
        return Proc.new {
            Prof::cons_show("RubyTest: timer fired.")
            Prof::cons_alert
        }
    end

    def self.cmd_upper
        return Proc.new { | line |
            win_tag = "Ruby Plygin"
            if (Prof::win_exists(win_tag) == false)
                Prof::win_create(win_tag, handle_upper)
            end
            Prof::win_focus(win_tag)
            if (line)
                handle_upper.call(win_tag, line)
            end
        }
    end

    def self.handle_upper
        return Proc.new { | win, line |
            upper = line.upcase
            Prof::win_show(win, upper)
            Prof::win_show_red(win, upper + " red")
            Prof::win_show_yellow(win, upper + " yellow")
            Prof::win_show_green(win, upper + " green")
            Prof::win_show_cyan(win, upper + " cyan")
        }
    end
end
