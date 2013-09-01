module ChatStart

    @@contacts = [
        "\"Prof 2\"",
        "prof3@panesar"
    ]

    def self.prof_on_connect(account_name, fulljid)
        @@contacts.each { | contact |
            Prof::send_line("/msg " + contact)
        }
        Prof::send_line("/win 1")
    end
end
