"""
Open the last link received in a chat or room window using the systems default browser
"""

import prof
import os
import webbrowser
import re

_links = {}
_lastlink = {}


def _cmd_browser(url):
    global _lastlink
    link = None

    # use arg if supplied
    if (url is not None):
        link = url
    else:
        jid = prof.get_current_recipient()
        room = prof.get_current_muc()

        # check if in chat window
        if (jid is not None):

            # check for link from recipient
            if jid in _lastlink.keys():
                link = _lastlink[jid]
            else:
                prof.cons_show("No links found from " + jid)

        # check if in muc window
        elif (room is not None):
            if room in _lastlink.keys():
                link = _lastlink[room]
            else:
                prof.cons_show("No links found from " + room)

        # not in chat/muc window
        else:
            prof.cons_show("You must supply a URL to the /browser command")

    # open the browser if link found
    if (link is not None):
        prof.cons_show("Opening " + link + " in browser")
        _open_browser(link)


def _open_browser(url):
    savout = os.dup(1)
    saverr = os.dup(2)
    os.close(1)
    os.close(2)
    os.open(os.devnull, os.O_RDWR)
    try:
        webbrowser.open(url, new=2)
    finally:
        os.dup2(savout, 1)
        os.dup2(saverr, 2)


def prof_init(version, status):
    synopsis = [ 
        "/browser",
        "/browser <url>"
    ]
    description = "View a URL in the systems default browser. If no argument is supplied, the last URL in the current chat or room will be used."
    args = [
        [ "<url>", "URL to open in the browser" ]
    ]
    examples = [
        "/browser http://www.profanity.im"
    ]

    prof.register_command("/browser", 0, 1, synopsis, description, args, examples, _cmd_browser)


def prof_on_chat_win_focus(jid):
    prof.completer_clear("/browser")
    if _links[jid]:
        prof.completer_add("/browser", _links[jid])


def prof_on_room_win_focus(room):
    prof.completer_clear("/browser")
    if _links[room]:
        prof.completer_add("/browser", _links[room])


def _process_message(jid, current_jid, message):
    links = re.findall(r'(https?://\S+)', message)
    if (len(links) > 0):
        if jid not in _links:
            _links[jid] = []
        # add to list of links for jid
        for link in links:
            if link not in _links[jid]:
                _links[jid].append(link)
        # add to autocompleter if message for current window
        if current_jid == jid:
            prof.completer_add("/browser", _links[jid])
        # set last link for jid
        _lastlink[jid] = links[len(links)-1]


def prof_post_chat_message_display(jid, message):
    current_jid = prof.get_current_recipient()
    _process_message(jid, current_jid, message)


def prof_post_room_message_display(room, nick, message):
    current_jid = prof.get_current_muc()
    _process_message(room, current_jid, message)


def prof_on_room_history_message(room, nick, message, timestamp):
    current_jid = prof.get_current_muc()
    _process_message(room, current_jid, message)
