import prof
import irc.client



def on_join(connection, event):
    main_loop(connection)


def on_connect(connection, event):
    if irc.client.is_channel(target):
        connection.join(target)
        return
	main_loop(connection)


def get_lines():
    while True:
        yield sys.stdin.readline().strip()


def main_loop(connection):
    for line in itertools.takewhile(bool, get_lines()):
        print(line)
        connection.privmsg(target, line)
    connection.quit("Using irc.client.py")


def on_disconnect(connection, event):
	raise SystemExit()


def prof_init(version, status, account_name, fulljid):
    reactor = irc.client.Reactor()
    try:
        c = reactor.server().connect("irc.freenode.net", 6665, "boothj5")
    except irc.client.ServerConnectionError:
        prof.cons_show(sys.exc_info()[1])

    c.add_global_handler("welcome", on_connect)
    c.add_global_handler("join", on_join)
    c.add_global_handler("disconnect", on_disconnect)

	reactor.process_forever()