import prof
import xml.etree.ElementTree as ET
import re

pubsub_win = "Pubsub"
iq_id_count = 1
registered_queries = {}
my_jid = ""

###
# commands
###

def _nodes(service, node = None):
    iq = _iq('get', service)

    query = ET.SubElement(iq, "query", {
        "xmlns": "http://jabber.org/protocol/disco#items"
    })
    if not node is None:
        query.set('node', node)

    _send(iq, _handle_disco_items)

def _handle_disco_items(service, iq):
    query = iq.find("{http://jabber.org/protocol/disco#items}query")
    if query is None:
        return True
    items = query.findall("{http://jabber.org/protocol/disco#items}item")
    if len(items) == 0:
        _show(service, "No items found.")
        return True
    _show(service, "Found items:")
    for el in items:
        prof.log_debug("got el: %s" % ET.tostring(el))
        node = el.get('node')
        name = el.get('name')
        if not node is None:
            _show(service, " - Node: %s" % node)
        else:
            _show(service, " - Name: %s" % name)
    return False

###

def _subscriptions(service, node = None):
    iq = _iq_pubsub('get', service, 'subscriptions', node)
    _send(iq, _handle_subscriptions)

def _handle_subscriptions(service, iq):
    #prof.log_debug("got subscriptions: %s" % ET.tostring(iq))
    pubsub = iq.find("{http://jabber.org/protocol/pubsub}pubsub")
    if pubsub is None:
        return True
    subscriptions = pubsub.findall("{http://jabber.org/protocol/pubsub}subscriptions/{http://jabber.org/protocol/pubsub}subscription")
    if len(subscriptions) == 0:
        _show(service, "You're not subscribed to any nodes")
        return False
    _show(service, "Got subscriptions:")
    for sub in subscriptions:
        _show(service, " - node: %s - subscription: %s - subid:%s" %
              (sub.get('node'), sub.get('subscription'), sub.get('subid')))
    return False

###

def _unsubscribe(service, node):
    global my_jid
    iq = _iq_pubsub('set', service, 'unsubscribe', node, {'jid': my_jid})
    _send(iq, _handle_unsubscribe)

def _handle_unsubscribe(service, iq):
    subscription = iq.find("{http://jabber.org/protocol/pubsub}pubsub/{http://jabber.org/protocol/pubsub}subscription")
    if subscription is None:
        _show(service, "Successfully unsubscribed.")
    elif subscription.get('subscription') == 'none':
        _show(service, "Successfully unsubscribed from %s" % subscription.get('node') )
    return False

###

def _subscribe(service, node):
    global my_jid
    iq = _iq_pubsub('set', service, 'subscribe', node, {'jid': my_jid})
    _send(iq, _handle_subscribe)

def _handle_subscribe(service, iq):
    subscription = iq.find("{http://jabber.org/protocol/pubsub}pubsub/{http://jabber.org/protocol/pubsub}subscription")
    if subscription is None:
        _show(service, "Successfully subscribed.")
        return False
    elif subscription.get('subscription') == 'subscribed':
        _show(service, "Successfully subscribed to %s" % subscription.get('node') )
        return False
    return True

###

def _items(service, node):
    iq = _iq_pubsub('get', service, 'items', node)
    _send(iq, _handle_items)

def _handle_items(service, iq):
    ps = iq.find("{http://jabber.org/protocol/pubsub}pubsub")
    if ps is None:
        return True
    itemsEl = ps.find("{http://jabber.org/protocol/pubsub}items")
    node = itemsEl.get('node')
    items = itemsEl.findall("{http://jabber.org/protocol/pubsub}item")
    for item in items:
        _show(service, _render_item(node, item))
    return False

def _render_item(node, item):
    message = "[%s] %s\n" % (node, item.get('id'))
    for child in item:
        childMsg = _render_child(child)
        if childMsg != '':
            message  = message + " - " + _render_child(child)
    return message

def _render_child(child):
    match child.tag:
        case '{urn:xmpp:serverinfo:0}serverinfo':
            return _render_serverinfo(child)
        case '{http://jabber.org/protocol/mood}mood':
            return _render_mood(child)
        case _:
            return child.tag

def _render_serverinfo(si):
    message = ''
    domains = si.findall('{urn:xmpp:serverinfo:0}domain')
    if domains is None:
        return messsage
    for domain in domains:
        remote_domains = domain.findall('{urn:xmpp:serverinfo:0}federation/{urn:xmpp:serverinfo:0}remote-domain')
        if remote_domains is None:
            message = "domain: %s (0 remote domains)\n" % domain.get('name')
            continue
        message = "domain: %s (%d remote domains)\n" % (domain.get('name'), len(remote_domains))
        for rdom in remote_domains:
            name = rdom.get('name')
            if name is None or name == '':
                name = "<anonymous>"
            message = message + "   + " + name + " ("
            connections = rdom.findall('{urn:xmpp:serverinfo:0}connection')
            if not connections is None:
                firstConn = True
                for conn in connections:
                    if not firstConn:
                        message = message + ", " + conn.get('type')
                    else:
                        message = message + conn.get('type')
                        firstConn = False
            message = message + ")\n"
    return message

def _render_mood(moodEl):
    mood = re.sub(r'{http://jabber.org/protocol/mood}', '', moodEl[0].tag)
    return "(%s) %s" % (mood, moodEl.find('{http://jabber.org/protocol/mood}text').text)

###
# prof callbacks
###
def prof_on_message_stanza_receive(stanza):
    msg = ET.fromstring(stanza)
    service = msg.get('from')
    if not msg.get('type') == 'headline':
        return True
    event = msg.find("{http://jabber.org/protocol/pubsub#event}event")
    if event is None:
        return True
    itemsEl = event.find("{http://jabber.org/protocol/pubsub#event}items")
    if itemsEl is None:
        prof.log_debug("pubsub event with no items: %s" % ET.tostring(event))
        return True
    _create_win(service)
    node = itemsEl.get('node')
    items = itemsEl.findall("{http://jabber.org/protocol/pubsub#event}item")
    for item in items:
        _show(service, _render_item(node, item))
    return False

def prof_on_iq_stanza_receive(stanza):
    iq = ET.fromstring(stanza)

    if not _valid_iq_result(iq):
        return True

    return _handle_iq_result(iq)

def _valid_iq_result(iq):
    if not iq.get("type") == "result":
        return False
    iq_id = iq.get("id")
    if not iq_id:
        return False
    try:
        registered = registered_queries[iq_id]
        sender = _bare_jid(iq.get('from'))
        if registered['remote'] != sender:
            return False
    except:
        return False
    return True

def _handle_iq_result(iq):
    iq_id = iq.get('id')
    service = iq.get('from')
    handler = registered_queries[iq_id]['handler']
    del registered_queries[iq_id]
    return handler(service, iq)

def _handle_win_input(win, command):
    prof.log_debug("win %s got command %s" % (win, command))
    service = _win_service(win)
    command = service + " " + command
    _cmd_pubsub(*command.split(' '))

def _cmd_pubsub(service, cmd = None, arg3 = None):
    prof.log_debug("pubsub cmd got args %s %s" % (service, cmd))

    win = _create_win(service)
    prof.win_focus(win)
    if cmd is None:
        return

    if not arg3 is None:
        _show(service, "Executing '%s %s'" % (cmd, arg3))
    else:
        _show(service, "Executing '%s'" % cmd)

    if cmd == "nodes":
        return _nodes(service, arg3)

    if cmd == "subscriptions":
        return _subscriptions(service, arg3)

    if cmd == 'subscribe' and not arg3 is None:
        return _subscribe(service, arg3)

    if cmd == 'unsubscribe' and not arg3 is None:
        return _unsubscribe(service, arg3)

    if cmd == 'items' and not arg3 is None:
        return _items(service, arg3)

    prof.cons_bad_cmd_usage("/pubsub")

def prof_init(version, status, account_name, fulljid):
    _set_my_jid(fulljid)
    synopsis = [
        "/pubsub <service>",
        "/pubsub <service> nodes [node]",
        "/pubsub <service> subscriptions [node]",
        "/pubsub <service> subscribe <node>",
        "/pubsub <service> unsubscribe <node>",
        "/pubsub <service> items <node>"
    ]
    description = "List, browse and subscribe/unsubscribe to/from pubsub nodes. There's a new window created for each service from which you can interact with it directly."
    args = [
        [ "<service>", "open service window"],
        [ "<service> nodes [node]", "list available nodes for service (or child nodes if 'node' given)"],
        [ "<service> subscriptions [node]", "list subscriptions"],
        [ "<service> subscribe <node>", "subscribe to node"],
        [ "<service> unsubscribe <node>", "unsubscribe from node"],
        [ "<service> items <node>", "retrieve items from node"]
    ]
    examples = [
        "/pubsub pubsub.jwchat.org nodes",
        "/pubsub pubsub.jwchat.org items serverinfo"
    ]

    prof.register_command("/pubsub", 1, 3, synopsis, description, args, examples, _cmd_pubsub)

def prof_on_connect(account_name, fulljid):
    _set_my_jid(fulljid)

#####
## helpers
#####
def _set_my_jid(jid = None):
    global my_jid
    if not jid is None and not jid == '':
        my_jid = _bare_jid(jid)
    prof.log_debug("my_jid: %s" % my_jid)

def _bare_jid(jid):
    return jid.split('/')[0]

def _create_win(service):
    win_name = _win_name(service)
    if prof.win_exists(win_name) == False:
        prof.win_create(win_name, _handle_win_input)
    return win_name

def _win_name(service):
    return f"{pubsub_win} %s" % service

def _win_service(name):
    return name.split(' ')[1]

def _show(service, msg):
    prof.win_show(_win_name(service), msg)

def _register_iq(iq, handler):
    global iq_id_count, registered_queries
    iq_id = "ps_" + str(iq_id_count)
    iq.set("id", iq_id)
    remote = _bare_jid(iq.get('to'))
    registered_queries[iq_id] = {'remote': remote, 'handler': handler}
    iq_id_count = iq_id_count + 1
    return iq

def _send(stanza, handler = None):
    if not handler is None:
        stanza = _register_iq(stanza, handler)
    prof.send_stanza(ET.tostring(stanza))

def _iq(type, to):
    return ET.Element("iq", {'type': type, 'to': to})

def _pubsub(el, child, node = None, attrs = None):
    pubsub = ET.SubElement(el, "pubsub", {"xmlns": "http://jabber.org/protocol/pubsub"})
    child_el = ET.SubElement(pubsub, child, {"xmlns": "http://jabber.org/protocol/pubsub"})
    if not node is None:
        child_el.set('node', node)
    if not attrs is None:
        for attr in attrs:
            child_el.set(attr, attrs[attr])
    return child_el

def _iq_pubsub(type, to, child, node, attrs = None):
    iq = _iq(type, to)
    _pubsub(iq, child, node, attrs)
    return iq
