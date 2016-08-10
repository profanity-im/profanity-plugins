import prof
from chatterbotapi import ChatterBotFactory, ChatterBotType


factory = ChatterBotFactory()
bot = factory.create(ChatterBotType.CLEVERBOT)
# bot = factory.create(ChatterBotType.JABBERWACKY)
# bot = factory.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')
bot_session = {}
bot_state = False


def prof_post_chat_message_display(barejid, resource, message):
    if bot_state:
        if barejid not in bot_session:
            bot_session[barejid] = bot.create_session()
        response = bot_session[barejid].think(message)
        prof.send_line("/msg " + barejid + " " + response)


def _cmd_chatterbot(state):
    global bot_state

    if state == "enable":
        prof.cons_show("ChatterBot Activated")
        bot_state = True
    elif state == "disable":
        prof.cons_show("ChatterBot Stopped")
        bot_state = False
    else:
        if bot_state:
            prof.cons_show("ChatterBot is running - current sessions:")
            prof.cons_show(str(bot_session))
        else:
            prof.cons_show("ChatterBot is stopped - /chatterbot enable to activate.")
        

def prof_init(version, status, account_name, fulljid):
    synopsis = [ 
        "/chatterbot",
        "/chatterbot enable|disable"
    ]
    description = "ChatterBot, running with no args will show the current chatterbot status"
    args = [
        [ "enable", "Enable chatterbot" ],
        [ "disable", "Disable chatterbot" ]
    ]
    examples = []

    prof.register_command("/chatterbot", 0, 1, synopsis, description, args, examples, _cmd_chatterbot)
    prof.completer_add("/chatterbot", [ "enable", "disable" ])
