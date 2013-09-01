module ChatStart

    @@starts = {
        "prof1@panesar" => [ "\"Prof 2\"", "prof3@panesar" ],
        "prof2@panesar" => [ "prof1@panesar" ]
    }

    def self.prof_on_connect(account_name, fulljid)
        if @@starts[account_name]
            @@starts[account_name].each { | contact |
                Prof::send_line("/msg " + contact)
            }
            Prof::send_line("/win 1")
        end
    end
end
