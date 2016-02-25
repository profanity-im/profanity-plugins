import prof
import getpass

def _cmd_whoami():
    me = getpass.getuser()
    prof.cons_show_themed("whoami", "result", None, me)

def prof_init(version, status):
    synopsis = [ "/whoami" ]
    description = "Calls the system whoami command"
    args = []
    examples = []

    prof.register_command("/whoami", 0, 0, synopsis, description, args, examples, _cmd_whoami)
