import prof
import subprocess

def _cmd_ascii(text):
    recipient = prof.get_current_recipient()
    if recipient:
        proc = subprocess.Popen(['figlet', '--', text], stdout=subprocess.PIPE)
        ascii_out = proc.communicate()[0].decode('utf-8')
        prof.send_line(u'\u000A' + ascii_out)

def prof_init(version, status):
    synopsis = [ "/ascii <message>" ]
    description = "ASCIIfy a message."
    args = [
        [ "<message>", "The message to be ASCIIfied" ]
    ]
    examples = [
        "/ascii \"Hello there\""
    ]
    
    prof.register_command("/ascii", 1, 1, synopsis, description, args, examples, _cmd_ascii)
