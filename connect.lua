local connect = {}

local user = "prof1@panesar"

function connect.prof_on_start()
    prof_cons_show("Enter password for " .. user)
    prof_send_line("/connect " ..  user)
end

return connect
