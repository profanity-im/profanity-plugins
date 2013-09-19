import prof
import platform

def _cmd_platform():
    result_summary = platform.platform()
    prof.cons_show(result_summary)

def prof_init(version, status):
    prof.register_command("/platform", 0, 0, "/platform", "Output system information.", "Output system information", _cmd_platform)
