"""
Manage jenkins jobs

Prerequisites:
The jenkinsapi module is required https://pypi.python.org/pypi/jenkinsapi
To install the module using pip:
    sudo pip install jenkinsapi

The plugin polls the jenkins server at 'jenkins_url' every 'poll_interval' seconds.
New failures are reported in the console, and a desktop notification is sent.

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
remind_interval = 20
jenkins_url = "http://localhost:8080"
username = None
password = None

failing = []
passing = []

def _show_help():
    global win_tag

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

def _list_jobs(j):
    global win_tag

    if len(j.keys()) == 0:
        prof.win_show(win_tag, "No jobs available")
        prof.win_show(win_tag, "")
    else:
        prof.win_show(win_tag, "Jobs:")
        for name, job in j.get_jobs():
            if job.is_queued():
                prof.win_show(win_tag, "  " + name + ", QUEUED")
            elif job.is_running():
                prof.win_show(win_tag, "  " + name + ", RUNNING")
            else:
                build = job.get_last_build_or_none()
                if build:
                    prof.win_show(win_tag, "  " + name + " #" + str(build.get_number()) + ", " + build.get_status())
                else:
                    prof.win_show(win_tag, "  " + name + ", no builds")
        prof.win_show(win_tag, "")

def _show_job(j, jobname=None):
    global win_tag

    if not jobname:
        prof.win_show(win_tag, "Usage: show [job]")
        prof.win_show(win_tag, "")
    else:
        if j.has_job(jobname):
            job = j.get_job(jobname)
            prof.win_show(win_tag, jobname + " details:");

            desc = job.get_description()
            if desc:
                prof.win_show  (win_tag, "  Description : " + desc)

            if job.is_queued():
                prof.win_show  (win_tag, "  Status      : Queued")
            elif job.is_running():
                prof.win_show  (win_tag, "  Status      : Running")
            else:
                build = job.get_last_build_or_none()
                if build:
                    prof.win_show  (win_tag, "  Last build  : #" + str(build.get_number()))
                    prof.win_show  (win_tag, "  Status      : " + build.get_status())
                else:
                    prof.win_show  (win_tag, "  Last build  : No builds")

            prof.win_show      (win_tag, "  Trigger     : " + job.get_build_triggerurl())
            prof.win_show(win_tag, "")
        else:
            prof.win_show(win_tag, "No such job " + jobname)
            prof.win_show(win_tag, "")

def _build_job(j, jobname):
    global win_tag

    if not jobname:
        prof.win_show(win_tag, "Usage: build [job]")
        prof.win_show(win_tag, "")
    else:
        if j.has_job(jobname):
            job = j.get_job(jobname)
            try:
                job.invoke(invoke_pre_check_delay=1)
            except Exception, e:
                prof.win_show(win_tag, "Failed to trigger build: " + str(e))
                prof.win_show(win_tag, "")
        else:
            prof.win_show(win_tag, "No such job " + jobname)
            prof.win_show(win_tag, "")

def _open_job(j, jobname):
    global win_tag

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
    global failing
    global passing
    global win_tag

    if not job.is_queued_or_running():
        build = job.get_last_build_or_none()
        if build:
            if build.get_status() == "FAILURE":
                if not name in failing:
                    prof.win_show(win_tag, name + " #" + str(build.get_number()) + " BROKEN")
                    prof.win_show(win_tag, "")
                    prof.notify(name + " BROKEN", 5000, "Jenkins")
                    failing.append(name)
                if name in passing:
                    passing.remove(name)
            else:
                if name in failing:
                    prof.win_show(win_tag, name + " #" + str(build.get_number()) + " FIXED")
                    prof.win_show(win_tag, "")
                    prof.notify(name + " FIXED", 5000, "Jenkins")
                    failing.remove(name)
                if not name in passing:
                    passing.append(name)

def _remind():
    global failing

    if len(failing) == 1:
        prof.notify("1 broken build", 5000, "Jenkins")
    if len(failing) > 1:
        prof.notify(str(len(failing)) + " broken builds", 5000, "Jenkins")

def _poll_jobs():
    global jenkins_url
    global username
    global password
    global win_tag

    try:
        j = Jenkins(jenkins_url, username, password)
    except Exception:
        prof.win_show(win_tag, "Jenkins down")
        prof.win_show(win_tag, "")
    else:
        for name, job in j.get_jobs():
            _process_job(name, job)

def _cmd_jenkins(cmd=None, jobname=None):
    global jenkins_url
    global username
    global password
    global win_tag

    if not prof.win_exists(win_tag):
        prof.win_create(win_tag, _handle_input)

    prof.win_focus(win_tag)

    if not cmd:
        _show_help()
    else:
        try:
            j = Jenkins(jenkins_url, username, password)
        except Exception:
            prof.win_show(win_tag, "Jenkins down")
            prof.win_show(win_tag, "")
        else:
            if cmd == "help":
                _show_help()
            elif cmd == "list":
                _list_jobs(j)
            elif cmd == "show":
                _show_job(j, jobname)
            elif cmd == "build":
                _build_job(j, jobname)
            elif cmd == "open":
                _open_job(j, jobname)
            else:
                prof.win_show(win_tag, "Usage: list|show|build|open [job].")
                prof.win_show(win_tag, "")

def prof_init(version, status):
    global poll_interval
    global win_tag

    prof.register_timed(_poll_jobs, poll_interval)
    prof.register_timed(_remind, remind_interval)
    prof.register_command("/jenkins", 0, 2, "/jenkins list|show|build|open [job]", "Do jenkins stuff.", "Do jenkins stuff.",
        _cmd_jenkins)

def _handle_input(win, line):
    _show_help()

def prof_on_start():
    global win_tag

    prof.win_create(win_tag, _handle_input)
    _show_help()

    try:
        j = Jenkins(jenkins_url, username, password)
    except Exception:
        prof.win_show(win_tag, "Jenkins down")
    else:
        _list_jobs(j)
