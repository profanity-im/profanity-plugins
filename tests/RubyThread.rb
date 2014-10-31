module RubyThread
    @counter = 0

    def self.inc_counter()
        while true
            sleep(1)
            @counter = @counter + 1
        end
    end

    def self.cmd_rcount()
        return Proc.new {
            instance_eval {
                Prof::cons_show("RCounter: " + @counter)
            }
        }
    end

    def self.prof_init(version, status)
        Thread.new { self.inc_counter() }
        Prof::register_command("/rcount", 0, 0, "/rcount", "Ruby threaded example", "Ruby threaded example", cmd_rcount)
    end
end
