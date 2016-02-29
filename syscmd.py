import prof
import subprocess

def _cmd_system(text):
    result = subprocess.Popen(text, shell=True, stdout=subprocess.PIPE).stdout.read()
    split = result.splitlines()
    for s in split:
        prof.cons_show(s)

def prof_init(version, status):
    synopsis = [ "/system <command>" ]
    description = "Run a system command."
    args = [
        [ "<command>", "The command" ]
    ]
    examples = [
        "/system \"ls -l\""
    ]
    prof.register_command("/system", 1, 1, synopsis, description, args, examples, _cmd_system)
