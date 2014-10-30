import prof
import os
import webbrowser
import re

_lastlink = {}

def _cmd_browser(url):
    global _lastlink
    link = None

    # use arg if supplied
    if (url != None):
        link = url
    else:
        jid = prof.get_current_recipient()

        # check if in chat window
        if (jid != None):

            # check for link from recipient
            if jid in _lastlink.keys():
                link = _lastlink[jid]
            else:
                prof.cons_show("No links found from " + jid)

        # not in chat window
        else:
            prof.cons_show("You must supply a URL to the /browser command")

    # open the browser if link found
    if (link != None):
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
    prof.register_command("/browser", 0, 1,
        "/browser [url]",
        "View a URL in the browser.",
        "View a URL in the browser, if no argument is supplied, " +
        "the last received URL will be used.",
        _cmd_browser)

def prof_post_chat_message_display(jid, message):
    global _lastlink
    links = re.findall(r'(https?://\S+)', message)
    if (len(links) > 0):
        _lastlink[jid] = links[len(links)-1]
