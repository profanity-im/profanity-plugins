"""
Play sounds on various events.
Default settings require mpg123 to be installed on the host system:
    sudo apt-get install mpg123
    brew install mpg123
"""

import subprocess
from os.path import expanduser

import prof


def _play_sound(soundfile):
    if soundfile.startswith("~/"):
        soundfilenew = soundfile.replace("~", expanduser("~"), 1)
    else:
        soundfilenew = soundfile

    audioplayer = prof.settings_string_get("sounds", "audioplayer", "mpg123 -q")
    subprocess.Popen([e for e in audioplayer.split(" ") + [soundfilenew]])


def _cmd_sounds(arg1=None, arg2=None, arg3=None):
    if not arg1:
        prof.cons_show("")
        enabled = prof.settings_boolean_get("sounds", "enabled", False)
        chatsound = prof.settings_string_get("sounds", "chat", None)
        roomsound = prof.settings_string_get("sounds", "room", None)
        privatesound = prof.settings_string_get("sounds", "private", None)
        roomlist = prof.settings_string_list_get("sounds", "rooms")
        audioplayer = prof.settings_string_get("sounds", "audioplayer", "mpg123 -q")

        if chatsound or roomsound or privatesound:
            if enabled:
                prof.cons_show("Sounds: ON")
            else:
                prof.cons_show("Sounds: OFF")

            prof.cons_show("Audio Player: " + audioplayer)
            if chatsound:
                prof.cons_show("  Chat    : " + chatsound)
            if roomsound:
                prof.cons_show("  Room    : " + roomsound)
                if roomlist and len(roomlist) > 0:
                    for room in roomlist:
                        prof.cons_show("    " + room)
                else:
                    prof.cons_show("    All rooms")
            if privatesound:
                prof.cons_show("  Private : " + privatesound)

        else:
            prof.cons_show("No sounds set.")
        
        return

    if arg1 == "on":
        prof.settings_boolean_set("sounds", "enabled", True)
        prof.cons_show("Sounds enabled")
        return

    if arg1 == "off":
        prof.settings_boolean_set("sounds", "enabled", False)
        prof.cons_show("Sounds disabled")
        return

    if arg1 == "test":
        if arg2 not in ("chat", "private", "room",):
            prof.cons_bad_cmd_usage("/sounds")
            return
    
        enabled = prof.settings_boolean_get("sounds", "enabled", False)
        if not enabled:
            prof.cons_show("Sounds disabled")
            return

        soundfile = prof.settings_string_get("sounds", arg2, None)
        if not soundfile:
            prof.cons_show("No sound file for " + arg2)
            return

        _play_sound(soundfile)
        return

    if arg1 == "set":
        if arg2 == "chat":
            prof.settings_string_set("sounds", "chat", arg3)
            prof.cons_show("Set chat sound: " + arg3)
        elif arg2 == "room":
            prof.settings_string_set("sounds", "room", arg3)
            prof.cons_show("Set room sound: " + arg3)
        elif arg2 == "private":
            prof.settings_string_set("sounds", "private", arg3)
            prof.cons_show("Set private sound: " + arg3)
        elif arg2 == "audioplayer":
            prof.settings_string_set("sounds", "audioplayer", arg3)
            prof.cons_show("Set audio player: " + arg3)
        else:
            prof.cons_bad_cmd_usage("/sounds")

        return

    if arg1 == "reset":
        if arg2 == "audioplayer":
            prof.settings_string_set("sounds", "audioplayer", "mpg123 -q")
            prof.cons_show("Reset audio player to default.")
        else:
            prof.cons_bad_cmd_usage("/sounds")

    if arg1 == "clear":
        if arg2 == "chat":
            prof.settings_string_set("sounds", "chat", "")
            prof.cons_show("Removed chat sound.")
        elif arg2 == "room":
            prof.settings_string_set("sounds", "room", "")
            prof.cons_show("Removed room sound.")
        elif arg2 == "private":
            prof.settings_string_set("sounds", "private", "")
            prof.cons_show("Removed private sound.")
        else:
            prof.cons_bad_cmd_usage("/sounds")

        return

    if arg1 == "rooms":
        if arg2 == "add":
            if not arg3:
                prof.cons_bad_cmd_usage("/sounds")
            else:
                prof.settings_string_list_add("sounds", "rooms", arg3)
                prof.cons_show("Sounds enabled for room: " + arg3)
        elif arg2 == "remove":
            if not arg3:
                prof.cons_bad_cmd_usage("/sounds")
            else:
                prof.settings_string_list_remove("sounds", "rooms", arg3)
                roomlist = prof.settings_string_list_get("sounds", "rooms")
                if roomlist and len(roomlist) > 0:
                    prof.cons_show("Sounds disabled for room: " + arg3)
                else:
                    prof.cons_show("Empty room list for sounds, playing in all rooms.")
        elif arg2 == "clear":
            prof.settings_string_list_clear("sounds", "rooms")
            prof.cons_show("Cleared sounds room list, playing in all rooms.")
        else:
            prof.cons_bad_cmd_usage("/sounds")

        return

    prof.cons_bad_cmd_usage("/sounds")


def prof_init(version, status, account_name, fulljid):
    synopsis = [ 
        "/sounds",
        "/sounds on|off",
        "/sounds set audioplayer <cmd>",
        "/sounds reset audioplayer",
        "/sounds set chat <file>",
        "/sounds set room <file>",
        "/sounds set private <file>",
        "/sounds test private|room|chat",
        "/sounds clear chat",
        "/sounds clear room",
        "/sounds clear private",
        "/sounds rooms add <roomjid>"
    ]
    description = "Play sounds on various Profanity events. Calling with no args shows current sound files."
    args = [
        [ "on|off", "Enable or disable playing sounds." ],
        [ "set audioplayer <cmd>", "Commmand line of audio player to use for playing sound files.  Defaults to mpg123."],
        [ "reset audioplayer", "Resets the audio player to the default mpg123." ],
        [ "set chat <file>", "Path to sound file to play on chat messages." ],
        [ "set room <file>", "Path to sound file to play on room messages." ],
        [ "set private <file>", "Path to sound file to play on private room messages." ],
        [ "test private|room|chat", "Test the configured audio player and sound file."],
        [ "clear chat", "Remove the sound for chat messages." ],
        [ "clear room", "Remove the sound for room messages." ],
        [ "clear private", "Remove the sound for private messages." ],
        [ "rooms add <roomjid>", "Add the room to the list that will play the room sound."],
        [ "rooms remove <roomjid>", "Remove the room from the list that will play the room sound."],
        [ "rooms clear", "Clear the room list, all rooms will play sounds on new messages."]
    ]
    examples = [
        "/sounds set audioplayer paplay",
        "/sounds set chat ~/sounds/woof.mp3",
        "/sounds set room ~/sounds/meow.mp3",
        "/sounds set private ~/sounds/shhh.mp3",
        "/sounds test private",
        "/sounds remove private",
        "/sounds rooms add myroom@conference.server.org",
        "/sounds on"
    ]

    prof.register_command("/sounds", 0, 3, synopsis, description, args, examples, _cmd_sounds)

    prof.completer_add("/sounds", [ "set", "clear", "on", "off", "rooms", "reset" ])
    prof.completer_add("/sounds set", [ "chat", "room", "private", "audioplayer" ])
    prof.completer_add("/sounds reset", [ "audioplayer" ])
    prof.completer_add("/sounds test", [ "chat", "room", "private" ])
    prof.completer_add("/sounds clear", [ "chat", "room", "private" ])
    prof.completer_add("/sounds rooms", [ "add", "remove", "clear" ])
    prof.filepath_completer_add("/sounds set chat")
    prof.filepath_completer_add("/sounds set room")
    prof.filepath_completer_add("/sounds set private")


def prof_post_chat_message_display(barejid, resource, message):
    enabled = prof.settings_boolean_get("sounds", "enabled", False)
    if not enabled:
        return

    soundfile = prof.settings_string_get("sounds", "chat", None)
    if not soundfile:
        return

    _play_sound(soundfile)


def prof_post_room_message_display(barejid, nick, message):
    my_nick = prof.get_room_nick(barejid)
    if not my_nick:
        return

    if my_nick == nick:
        return;

    enabled = prof.settings_boolean_get("sounds", "enabled", False)
    if not enabled:
        return

    soundfile = prof.settings_string_get("sounds", "room", None)
    if not soundfile:
        return

    roomlist = prof.settings_string_list_get("sounds", "rooms")
    if roomlist and (barejid not in roomlist):
        return

    _play_sound(soundfile)


def prof_post_priv_message_display(barejid, nick, message):
    enabled = prof.settings_boolean_get("sounds", "enabled", False)
    if not enabled:
        return

    soundfile = prof.settings_string_get("sounds", "private", None)
    if soundfile:
        _play_sound(soundfile)

