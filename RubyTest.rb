module RubyTest

    def self.prof_init(version, status)
        Prof::cons_show("RubyTest: init, " + version + ", " + status)
        Prof::register_command("/ruby", 0, 1, "/ruby", "RubyTest", "RubyTest", cmd_ruby)
        Prof::register_command("/lower", 0, 1, "/lower", "Lowercase input string", "Lowercase input string", cmd_lower)
        Prof::register_timed(timer_test, 10)
    end

    def self.prof_on_start()
        Prof::cons_show("RubyTest: on_start")
        Prof::log_debug("RubyTest: logged debug");
        Prof::log_info("RubyTest: logged info");
        Prof::log_warning("RubyTest: logged warning");
        Prof::log_error("RubyTest: logged error");
    end

    def self.prof_on_connect(account_name, fulljid)
        Prof::cons_show("RubyTest: on_connect, " + account_name + ", " + fulljid)
    end

    def self.prof_on_disconnect(account_name, fulljid)
        Prof::cons_show("RubyTest: on_disconnect, " + account_name + ", " + fulljid)
        Prof::log_info("RubyTest: on_disconnect, " + account_name + ", " + fulljid)
    end

    def self.prof_on_message_received(jid, message)
        Prof::cons_show("RubyTest: on_message_received, " + jid + ", " + message)
        Prof::cons_alert
        return message + "[RUBY]"
    end

    def self.prof_on_room_message_received(room, nick, message)
        Prof::cons_show("RubyTest: on_room_message_received, " + room + ", " + nick + ", " + message)
        Prof::cons_alert
        return message + "[RUBY]"
    end

    def self.prof_on_private_message_received(room, nick, message)
        Prof::cons_show("RubyTest: on_private_message_received, " + room + ", " + nick + ", " + message)
        Prof::cons_alert
        return message + "[RUBY]"
    end

    def self.prof_on_message_send(jid, message)
        Prof::cons_show("RubyTest: on_message_send, " + jid + ", " + message)
        Prof::cons_alert
        return message + "[RUBY]"
    end

    def self.prof_on_private_message_send(room, nick, message)
        Prof::cons_show("RubyTest: on_private_message_send, " + room + ", " + nick + ", " + message)
        Prof::cons_alert
        return message + "[RUBY]"
    end

    def self.prof_on_room_message_send(room, message)
        Prof::cons_show("RubyTest: on_room_message_send, " + room + ", " + message)
        Prof::cons_alert
        return message + "[RUBY]"
    end

    def self.prof_on_shutdown()
        Prof::log_info("RubyTest: on_shutdown");
    end

    def self.cmd_ruby()
        return Proc.new { | msg |
            if msg
                Prof::cons_show("RubyTest: /ruby command called, arg = " + msg)
            else
                Prof::cons_show("RubyTest: /ruby command called with no arg")
            end
            Prof::cons_alert
            Prof::notify("RubyTest: notify", 2000, "Plugins")
            Prof::send_line("/help")
            Prof::cons_show("RubyTest: sent \"/help\" command")
        }
    end

    def self.timer_test()
        return Proc.new {
            Prof::cons_show("RubyTest: timer fired.")
            recipient = Prof::get_current_recipient
            if recipient
                Prof::cons_show("  current recipient = " + recipient)
            end
            Prof::cons_alert
        }
    end

    def self.cmd_lower()
        return Proc.new { | line |
            win_tag = "Lower echo"
            if (Prof::win_exists(win_tag) == false)
                Prof::win_create(win_tag, handle_lower)
            end

            Prof::win_focus(win_tag)

            if (line)
                Prof::win_process_line(win_tag, line)
            end
        }
    end

    def self.handle_lower()
        return Proc.new { | win, line |
            Prof::win_show(win, line.downcase)
        }
    end
end
