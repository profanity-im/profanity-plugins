"""
Requires wikipedia API
    pip install wikipedia

Example theme options (~/.local/share/profanity/plugin_themes):

[wikipedia]
error=red
search=bold_green
search.noresult=red
search.results=green
summary.nopage=red
summary.title=bold_green
summary.url=magenta
summary.text=cyan
page.nopage=red
page.title=bold_green
page.text=cyan
images.nopage=red
images=bold_green
images.url=magenta
links.nopage=red
links=bold_green
links.link=green
refs.nopage=red
refs=bold_green
refs.url=magenta

"""

import prof

import wikipedia
import os
import webbrowser
import requests

win = "Wikipedia"
page_ac = []
link_ac = []


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


def _handle_win_input():
    pass


def create_win():
    if prof.win_exists(win) == False:
        prof.win_create(win, _handle_win_input)


def _update_autocomplete():
    prof.completer_add("/wikipedia page", page_ac)
    prof.completer_add("/wikipedia summary", page_ac)
    prof.completer_add("/wikipedia images", page_ac)
    prof.completer_add("/wikipedia links", page_ac)
    prof.completer_add("/wikipedia refs", page_ac)


def _search(search_terms):
    global page_ac

    results = wikipedia.search(search_terms)
    create_win()
    if len(results) > 0:
        prof.win_show_themed(win, "wikipedia", "search", None, "Search results for \"" + search_terms + "\":")
        for index, result in enumerate(results):
            page_ac.append(result)
            prof.win_show_themed(win, "wikipedia", "search.results", None, result)
        _update_autocomplete()
    else:
        prof.win_show_themed(win, "wikipedia", "search.noresults", None, "No search results found for \"" + search_terms + "\"")
    prof.win_show(win, "")
    prof.win_focus(win)


def _summary(page_str):
    global link_ac

    page = wikipedia.page(page_str)
    create_win()
    if not page:
        prof.win_show_themed(win, "wikipedia", "summary.nopage", None, "No such page: \"" + page_str + "\"")
        prof.win_show(win, "")
        prof.win_focus(win)
        return

    link_ac.append(page.url)
    prof.completer_add("/wikipedia open", link_ac)

    prof.win_show_themed(win, "wikipedia", "summary.title", None, page.title)
    prof.win_show_themed(win, "wikipedia", "summary.url", None, page.url)

    summary = wikipedia.summary(page_str)
    prof.win_show_themed(win, "wikipedia", "summary.text", None, summary)
    prof.win_show(win, "")
    prof.win_focus(win)


def _page(page_str):
    page = wikipedia.page(page_str)
    create_win()
    if not page:
        prof.win_show_themed(win, "wikipedia", "page.nopage", None, "No such page: \"" + page_str + "\"")
        prof.win_show(win, "")
        prof.win_focus(win)
        return

    prof.win_show_themed(win, "wikipedia", "page.title", None, page.title)
    prof.win_show_themed(win, "wikipedia", "page.text", None, page.content)
    prof.win_show(win, "")
    prof.win_focus(win)


def _images(page_str):
    global link_ac

    page = wikipedia.page(page_str)
    create_win()
    if not page:
        prof.win_show_themed(win, "wikipedia", "images.nopage", None, "No such page: \"" + page_str + "\"")
        prof.win_show(win, "")
        prof.win_focus(win)
        return

    prof.win_show_themed(win, "wikipedia", "images", None, "Images for " + page_str)
    for image in page.images:
        prof.win_show_themed(win, "wikipedia", "images.url", None, image)
        link_ac.append(image)
    prof.completer_add("/wikipedia open", link_ac)
    prof.win_show(win, "")
    prof.win_focus(win)


def _links(page_str):
    global page_ac

    page = wikipedia.page(page_str)
    create_win()
    if not page:
        prof.win_show_themed(win, "wikipedia", "links.nopage", None, "No such page: \"" + page_str + "\"")
        prof.win_show(win, "")
        prof.win_focus(win)
        return

    prof.win_show_themed(win, "wikipedia", "links", None, "Links for " + page_str)

    for link in page.links:
        prof.win_show_themed(win, "wikipedia", "links.link", None, link)
        page_ac.append(link)
    _update_autocomplete()
    prof.win_show(win, "")
    prof.win_focus(win)


def _refs(page_str):
    global link_ac

    page = wikipedia.page(page_str)
    create_win()
    if not page:
        prof.win_show_themed(win, "wikipedia", "refs.nopage", None, "No such page: \"" + page_str + "\"")
        prof.win_show(win, "")
        prof.win_focus(win)
        return

    prof.win_show_themed(win, "wikipedia", "refs", None, "References for " + page_str)
    for ref in page.references:
        prof.win_show_themed(win, "wikipedia", "refs.url", None, ref)
        link_ac.append(ref)
    prof.completer_add("/wikipedia open", link_ac)
    prof.win_show(win, "")
    prof.win_focus(win)


def cmd_wp(subcmd, arg):
    try:
        if   subcmd == "search":    _search(arg)
        elif subcmd == "summary":   _summary(arg)
        elif subcmd == "page":      _page(arg)
        elif subcmd == "images":    _images(arg)
        elif subcmd == "links":     _links(arg)
        elif subcmd == "refs":      _refs(arg)
        elif subcmd == "open":      _open_browser(arg)
    except wikipedia.exceptions.WikipediaException as e:
        create_win()
        prof.win_show_themed(win, "wikipedia", "error", None, str(e))
        prof.win_show(win, "")
        prof.win_focus(win)
    except requests.exceptions.ConnectionError:
        create_win()
        prof.win_show_themed(win, "wikipedia", "error", None, "Connection Error")
        prof.win_show(win, "")
        prof.win_focus(win)


def prof_init(version, status, account_name, fulljid):
    synopsis = [
        "/wikipedia search <text>",
        "/wikipedia summary <title>",
        "/wikipedia page <title>",
        "/wikipedia images <title>",
        "/wikipedia links <title>",
        "/wikipedia refs <title>",
        "/wikipedia open <url>"
    ]
    description = "Interact with wikipedia."
    args = [
        [ "search <text>",  "Search for pages" ],
        [ "summary <title>", "Show summary for page" ],
        [ "page <title>",    "Show the whole page" ],
        [ "images <title>",  "Show images URLs for page" ],
        [ "links <title>",   "Show links to other pages from page" ],
        [ "refs <title>",   "Show external references for page" ],
        [ "open <url>",     "Open the a URL in the browser" ]
    ]
    examples = [
        "/wikipedia search Iron Maiden"
    ]

    prof.register_command("/wikipedia", 2, 2, synopsis, description, args, examples, cmd_wp)

    prof.completer_add("/wikipedia", 
        [ "search", "summary", "page", "images", "links", "refs", "open" ]
    )
