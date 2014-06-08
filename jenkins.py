"""
Manage jenkins jobs

Prerequisites:
The jenkinsapi module is required https://pypi.python.org/pypi/jenkinsapi
To install the module using pip:
    sudo pip install jenkinsapi

The plugin polls the jenkins server at 'jenkins_url' every 'poll_interval' seconds.
New failures are reported in the jenkins window, and a desktop notification is sent.

The 'remind_interval' specified the time between reminder notifications of broken builds

Both intervals can be disabled with a value of 0, which means builds must be checked manually using
the supplied commands.

The following commands are available:

/jenkins jobs - list all jobs
/jenkins show [job] - show details of a specific job
/jenkins build [job] - trigger a build for the job
/jenkins open [job] - open the job in the systems default browser

"""

import prof
import os
import webbrowser
import jenkinsapi
from jenkinsapi.jenkins import Jenkins

win_tag = "Jenkins"
poll_interval = 10
remind_interval = 60 * 15
enable_remind = True
jenkins_url = "http://localhost:8080"
username = None
password = None

last_state = {}
STATE_SUCCESS = "SUCCESS"
STATE_UNSTABLE = "UNSTABLE"
STATE_FAILURE = "FAILURE"
STATE_QUEUED = "QUEUED"
STATE_RUNNING = "RUNNING"
STATE_NOBUILDS = "NOBUILDS"
STATE_UNKNOWN = "UNKNOWN"

def _show_help():
    prof.win_show(win_tag, "Commands:")
    prof.win_show(win_tag, "  /jenkins help        - Show this help")
    prof.win_show(win_tag, "  /jenkins list        - List all jobs")
    prof.win_show(win_tag, "  /jenkins show [job]  - Details of specific job")
    prof.win_show(win_tag, "  /jenkins build [job] - Trigger build for job")
    prof.win_show(win_tag, "  /jenkins open [job]  - Open job in browser")
    prof.win_show(win_tag, "")

def _open_job_url(url):
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

def _safe_remove(jobname, state):
    if jobname in last_state[state]:
        last_state[state].remove(jobname)

def _set_state(jobname, state):
    if not jobname in last_state[state]:
        _safe_remove(jobname, STATE_SUCCESS)
        _safe_remove(jobname, STATE_UNSTABLE)
        _safe_remove(jobname, STATE_FAILURE)
        _safe_remove(jobname, STATE_QUEUED)
        _safe_remove(jobname, STATE_RUNNING)
        _safe_remove(jobname, STATE_NOBUILDS)
        _safe_remove(jobname, STATE_UNKNOWN)
        last_state[state].append(jobname)
        return True
    else:
        return False

def _list_jobs():
    try:
        j = Jenkins(jenkins_url, username, password)
    except Exception, e:
        prof.log_warning("Could not connect to jenkins: " + str(e))
        prof.win_show(win_tag, "Could not connect to Jenkins.")
        prof.win_show(win_tag, "")
    else:
        if len(j.keys()) == 0:
            prof.win_show(win_tag, "No jobs available")
            prof.win_show(win_tag, "")
        else:
            prof.win_show(win_tag, "Jobs:")
            for name, job in j.get_jobs():
                if job.is_queued():
                    _set_state(name, STATE_QUEUED)
                    prof.win_show_cyan(win_tag, "  " + name + ", QUEUED")
                elif job.is_running():
                    _set_state(name, STATE_RUNNING)
                    prof.win_show_cyan(win_tag, "  " + name + ", RUNNING")
                else:
                    build = job.get_last_build_or_none()
                    if build:
                        if build.get_status() == "FAILURE":
                            _set_state(name, STATE_FAILURE)
                            prof.win_show_red(win_tag, "  " + name + " #" + str(build.get_number()) + ", " + build.get_status())
                        elif build.get_status() == "SUCCESS":
                            _set_state(name, STATE_SUCCESS)
                            prof.win_show_green(win_tag, "  " + name + " #" + str(build.get_number()) + ", " + build.get_status())
                        elif build.get_status() == "UNSTABLE":
                            _set_state(name, STATE_UNSTABLE)
                            prof.win_show_yellow(win_tag, "  " + name + " #" + str(build.get_number()) + ", " + build.get_status())
                        else:
                            _set_state(name, STATE_UNKNOWN)
                            prof.win_show_cyan(win_tag, "  " + name + " #" + str(build.get_number()) + ", " + build.get_status())
                    else:
                        _set_state(name, STATE_NOBUILDS)
                        prof.win_show(win_tag, "  " + name + ", no builds")
            prof.win_show(win_tag, "")

def _show_job(jobname):
    try:
        j = Jenkins(jenkins_url, username, password)
    except Exception, e:
        prof.log_warning("Could not connect to jenkins: " + str(e))
        prof.win_show(win_tag, "Could not connect to Jenkins.")
        prof.win_show(win_tag, "")
    else:
        if j.has_job(jobname):
            job = j.get_job(jobname)
            prof.win_show(win_tag, jobname + " details:");

            desc = job.get_description()
            if desc:
                prof.win_show(win_tag, "  Description : " + desc)

            if job.is_queued():
                _set_state(jobname, STATE_QUEUED)
                prof.win_show_cyan(win_tag, "  Status      : Queued")
            elif job.is_running():
                _set_state(jobname, STATE_RUNNING)
                prof.win_show_cyan(win_tag, "  Status      : Running")
            else:
                build = job.get_last_build_or_none()
                if build:
                    prof.win_show(win_tag, "  Last build  : #" + str(build.get_number()))
                    if build.get_status() == "FAILURE":
                        _set_state(jobname, STATE_FAILURE)
                        prof.win_show_red(win_tag, "  Status      : " + build.get_status())
                    elif build.get_status() == "SUCCESS":
                        _set_state(jobname, STATE_SUCCESS)
                        prof.win_show_green(win_tag, "  Status      : " + build.get_status())
                    elif build.get_status() == "UNSTABLE":
                        _set_state(jobname, STATE_UNSTABLE)
                        prof.win_show_yellow(win_tag, "  Status      : " + build.get_status())
                    else:
                        _set_state(jobname, STATE_UNKNOWN)
                        prof.win_show_cyan(win_tag, "  Status      : " + build.get_status())
                else:
                    _set_state(jobname, STATE_NOBUILDS)
                    prof.win_show(win_tag, "  Last build  : No builds")

            prof.win_show(win_tag, "  Trigger     : " + job.get_build_triggerurl())
            prof.win_show(win_tag, "")
        else:
            prof.win_show(win_tag, "No such job " + jobname)
            prof.win_show(win_tag, "")

def _build_job(jobname):
    try:
        j = Jenkins(jenkins_url, username, password)
    except Exception, e:
        prof.log_warning("Could not connect to jenkins: " + str(e))
        prof.win_show(win_tag, "Could not connect to Jenkins.")
        prof.win_show(win_tag, "")
    else:
        if j.has_job(jobname):
            job = j.get_job(jobname)
            try:
                job.invoke(invoke_pre_check_delay=1)
            except Exception, e:
                prof.log_warning("Failed to trigger build: " + str(e))
                prof.win_show(win_tag, "Failed to trigger build.")
                prof.win_show(win_tag, "")
        else:
            prof.win_show(win_tag, "No such job " + jobname)
            prof.win_show(win_tag, "")

def _open_job(jobname):
    try:
        j = Jenkins(jenkins_url, username, password)
    except Exception, e:
        prof.log_warning("Could not connect to jenkins: " + str(e))
        prof.win_show(win_tag, "Could not connect to Jenkins.")
        prof.win_show(win_tag, "")
    else:
        if not jobname:
            prof.win_show(win_tag, "Usage: open [job]")
            prof.win_show(win_tag, "")
        else:
            if j.has_job(jobname):
                _open_job_url(jenkins_url + "/job/" + jobname)
            else:
                prof.win_show(win_tag, "No such job " + jobname)
                prof.win_show(win_tag, "")

def _process_job(name, job):
    if not job.is_queued_or_running():
        build = job.get_last_build_or_none()
        if build:
            if build.get_status() == "FAILURE":
                changed = _set_state(name, STATE_FAILURE)
                if changed:
                    prof.win_show_red(win_tag, name + " #" + str(build.get_number()) + " FAILURE")
                    prof.win_show(win_tag, "")
                    prof.notify(name + " FAILURE", 5000, "Jenkins")
            elif build.get_status() == "SUCCESS":
                changed = _set_state(name, STATE_SUCCESS)
                if changed:
                    prof.win_show_green(win_tag, name + " #" + str(build.get_number()) + " SUCCESS")
                    prof.win_show(win_tag, "")
                    prof.notify(name + " SUCCESS", 5000, "Jenkins")
            elif build.get_status() == "UNSTABLE":
                changed = _set_state(name, STATE_UNSTABLE)
                if changed:
                    prof.win_show_yellow(win_tag, name + " #" + str(build.get_number()) + " UNSTABLE")
                    prof.win_show(win_tag, "")
                    prof.notify(name + " UNSTABLE", 5000, "Jenkins")
    else:
        if job.is_queued():
            changed = _set_state(name, STATE_QUEUED)
            if changed:
                prof.win_show_cyan(win_tag, name + " QUEUED")
                prof.win_show(win_tag, "")
        elif job.is_running():
            changed = _set_state(name, STATE_RUNNING)
            if changed:
                prof.win_show_cyan(win_tag, name + " RUNNING")
                prof.win_show(win_tag, "")

def _remind():
    if enable_remind:
        notify_string = ""
        failing = len(last_state[STATE_FAILURE])
        unstable = len(last_state[STATE_UNSTABLE]) 

        if failing == 1:
            notify_string = notify_string + "1 failing build"
        if failing > 1:
            notify_string = notify_string + str(failing) + " failing builds"

        if failing > 0 and unstable > 0:
            notify_string = notify_string + "\n"

        if unstable == 1:
            notify_string = notify_string + "1 unstable build"
        if unstable > 1:
            notify_string = notify_string + str(unstable) + " unstable builds"

        if not notify_string == "":
            prof.notify(notify_string, 5000, "Jenkins")

def _poll_jobs():
    try:
        j = Jenkins(jenkins_url, username, password)
    except Exception, e:
        prof.log_warning("Could not connect to jenkins: " + str(e))
        prof.win_show(win_tag, "Could not connect to Jenkins.")
        prof.win_show(win_tag, "")
    else:
        for name, job in j.get_jobs():
            _process_job(name, job)

def _cmd_jenkins(cmd=None, arg=None):
    global enable_remind

    if not prof.win_exists(win_tag):
        prof.win_create(win_tag, _handle_input)

    prof.win_focus(win_tag)

    if not cmd:
        _show_help()
    else:
        try:
            j = Jenkins(jenkins_url, username, password)
        except Exception, e:
            prof.log_warning("Could not connect to jenkins: " + str(e))
            prof.win_show(win_tag, "Could not connect to Jenkins.")
            prof.win_show(win_tag, "")
        else:
            if cmd == "help":
                _show_help()
            elif cmd == "list":
                _list_jobs()
            elif cmd == "show":
                if not arg:
                    prof.win_show(win_tag, "Usage: show [job]")
                    prof.win_show(win_tag, "")
                else:
                    _show_job(arg)
            elif cmd == "build":
                if not arg:
                    prof.win_show(win_tag, "Usage: build [job]")
                    prof.win_show(win_tag, "")
                else:
                    _build_job(arg)
            elif cmd == "open":
                if not arg:
                    prof.win_show(win_tag, "Usage: open [job]")
                    prof.win_show(win_tag, "")
                else:
                    _open_job(arg)
            elif cmd == "remind":
                if not arg:
                    prof.win_show(win_tag, "Usage: remind on|off")
                else:
                    if arg == "on":
                        enable_remind = True
                        prof.win_show(win_tag, "Reminders enabled.")
                    elif arg == "off":
                        enable_remind = False
                        prof.win_show(win_tag, "Reminders disabled.")
                    else:
                        prof.win_show(win_tag, "Usage: remind on|off")
                prof.win_show(win_tag, "")
            else:
                prof.win_show(win_tag, "Usage: list|show|build|open|remind")
                prof.win_show(win_tag, "")

def prof_init(version, status):
    last_state[STATE_SUCCESS] = []
    last_state[STATE_UNSTABLE] = []
    last_state[STATE_FAILURE] = []
    last_state[STATE_QUEUED] = []
    last_state[STATE_RUNNING] = []
    last_state[STATE_NOBUILDS] = []
    last_state[STATE_UNKNOWN] = []

    if poll_interval > 0:
        prof.register_timed(_poll_jobs, poll_interval)
    if remind_interval > 0:
        prof.register_timed(_remind, remind_interval)
    prof.register_command("/jenkins", 0, 2, "/jenkins list|show|build|open|remind", "Do jenkins stuff.", "Do jenkins stuff.",
        _cmd_jenkins)

def _handle_input(win, line):
    _show_help()

def prof_on_start():
    prof.win_create(win_tag, _handle_input)
    _show_help()
    _list_jobs()
