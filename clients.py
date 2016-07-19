import prof
import xml.etree.ElementTree as ET

clients_win = "Clients"
iq_id_count = 1


def _handle_win_input(win, command):
    pass


def _create_win():
    if prof.win_exists(clients_win) == False:
        prof.win_create(clients_win, _handle_win_input)


def prof_on_iq_stanza_receive(stanza):
    iq = ET.fromstring(stanza)
    iq_id = iq.get("id")
    if not iq_id:
        return True
    if not iq_id.startswith("clients_"):
        return True

    iq_type = iq.get("type")
    if not iq_type:
        return True
    if iq_type != "result":
        return True

    iq_from = iq.get("from")
    if not iq_from:
        return True

    query = iq.find("{jabber:iq:version}query")
    if query is None:
        return True

    name = query.find("{jabber:iq:version}name")
    version = query.find("{jabber:iq:version}version")
    if name is None and version is None:
        return True

    message = iq_from.split("/")[1]
    if name is not None:
        message = message + ", " + name.text
    if version is not None:
        message = message + ", " + version.text

    prof.win_show(clients_win, message)

    return False


def _sv_send(muc, occupant):
    global iq_id_count

    iq = ET.Element("iq", {
        "type": "get",
        "to":   muc + "/" + occupant,
        "id":   "clients_" + str(iq_id_count)  
    })
    ET.SubElement(iq, "query", {
        "xmlns": "jabber:iq:version"
    })

    iq_id_count = iq_id_count + 1

    prof.send_stanza(ET.tostring(iq).decode("utf-8"))


def _cmd_clients():
    muc = prof.get_current_muc()
    if muc == None:
        prof.cons_show("Command only valid in chat rooms.")
        return
	
    occupants = prof.get_current_occupants()
    if occupants == None or len(occupants) == 0:
        prof.cons_show("No occupants for /clients command.")
        return

    nick = prof.get_current_nick()

    _create_win()
    prof.win_focus(clients_win)

    for occupant in occupants:
        if nick != occupant:
            _sv_send(muc, occupant)


def prof_init(version, status, account_name, fulljid):
    synopsis = [ 
        "/clients"
    ]
    description = "Show client software used by chat room occupants"
    args = []
    examples = []

    prof.register_command("/clients", 0, 0, synopsis, description, args, examples, _cmd_clients)
