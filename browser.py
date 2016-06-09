"""
Open the last link received in a chat or room window using the systems default browser
"""

import prof
import os
import webbrowser
import re
import requests
from os.path import expanduser

_links = {}
_lastlink = {}


def _get_url():
    link = None
    jid = prof.get_current_recipient()
    room = prof.get_current_muc()

    # check if in chat window
    if jid is not None:

        # check for link from recipient
        if jid in _lastlink.keys():
            link = _lastlink[jid]
        else:
            prof.cons_show("No links found from " + jid)

    # check if in muc window
    elif room is not None:
        if room in _lastlink.keys():
            link = _lastlink[room]
        else:
            prof.cons_show("No links found in " + room)

    # not in chat/muc window
    else:
        prof.cons_show("You must supply a URL to the /browser command")

    return link

def _cmd_browser(arg1=None, arg2=None):
    global _lastlink
    link = None

    if arg1 == "setdir":
        if not arg2:
            prof.cons_bad_cmd_usage("/browser")
        else:
            prof.settings_set_string("browser", "download.path", arg2)
            prof.cons_show("browser.py set download path to" + arg2)

        return

    if arg1 == "get":
        link = arg2 if arg2 is not None else _get_url()

        if not link:
            prof.log_debug("browser.py: no link found for get command")
            return

        folder = prof.settings_get_string("browser", "download.path", "")
        if folder == "":
            prof.cons_show("Download path not set, see /help browser")
            return

        if folder[0] == '~':
            folder = expanduser("~") + folder[1:]

        response = requests.get(link)
        if response.status_code != 200:
            prof.log_debug("browser.py: received non 200 response for get command")
            return

        filename = link.split("/")[-1]
        full_path = folder + "/" + filename
        prof.log_debug("browser.py: Saving link {link} to file {file}".format(link=link, file=full_path))
        with open(full_path, 'wb') as f:
            for chunk in response.iter_content(8):
                f.write(chunk)

        return

    link = arg1 if arg1 is not None else _get_url();
    if link is not None:
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


def prof_init(version, status, account_name, fulljid):
    synopsis = [ 
        "/browser",
        "/browser <url>",
        "/browser get <url>",
        "/browser setdir <folder>"
    ]
    description = (
        "View a URL in the systems default browser, or download and view link contents " + 
        "If no argument is supplied, the last URL in the current chat or room will be used. " + 
        "Tab autocompletion will go through all previous links in the current chat/room"
    )
    args = [
        [ "<url>",          "URL to open in the browser" ],
        [ "download <url>", "Download contents of specified URL" ],
        [ "setdir <dir>",   "Filesystem path to store downloaded content" ]
    ]
    examples = [
        "/browser http://www.profanity.im",
        "/browser setdir ~/Downloads",
        "/browser get http://www.movenoticias.com/wp-content/uploads/2015/05/Bruce-Iron-Maiden-850x583.jpg"
    ]

    prof.register_command("/browser", 0, 2, synopsis, description, args, examples, _cmd_browser)
    prof.completer_add("/browser", [ "get", "setdir" ])


def prof_on_chat_win_focus(jid):
    prof.completer_clear("/browser")
    if jid in _links:
        prof.completer_add("/browser", _links[jid])


def prof_on_room_win_focus(room):
    prof.completer_clear("/browser")
    if room in _links:
        prof.completer_add("/browser", _links[room])


def _process_message(jid, current_jid, message):
    links = re.findall(r'(https?://\S+)', message)
    if len(links) > 0:
        if jid not in _links:
            _links[jid] = []
        
        # add to list of links for jid
        for link in links:
            if link not in _links[jid]:
                prof.log_debug("browser.py: Saving {link} for {jid}".format(link=link, jid=jid))
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
