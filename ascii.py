import prof
import subprocess

def _cmd_ascii(text):
    recipient = prof.get_current_recipient()
    if recipient:
        proc = subprocess.Popen(['figlet', '--', text], stdout=subprocess.PIPE)
        ascii_out = proc.communicate()[0].decode('utf-8')
        prof.send_line(u'\u000A' + ascii_out)

def prof_init(version, status):
    prof.register_command("/ascii", 1, 1, "/ascii", "ASCIIfy a message", "ASCIIfy a message.", _cmd_ascii)
