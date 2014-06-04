import prof
import os
import webbrowser
import jenkinsapi
from jenkinsapi.jenkins import Jenkins

jenkins_url = "http://localhost:8080"
username = None
password = None

failing = []
passing = []

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
    if len(j.keys()) == 0:
        prof.cons_show("Jenkins: No jobs available")
    else:
        prof.cons_show("")
        prof.cons_show("Jenkins jobs:")
        for name, job in j.get_jobs():
            if job.is_queued():
                prof.cons_show("  " + name + ", QUEUED")
            elif job.is_running():
                prof.cons_show("  " + name + ", RUNNING")
            else:
                build = job.get_last_build_or_none()
                if build:
                    prof.cons_show("  " + name + " #" + str(build.get_number()) + ", " + build.get_status())
                else:
                    prof.cons_show("  " + name + ", no builds")
        prof.cons_show("")

def _show_job(j, jobname):
    if not jobname:
        prof.cons_show("Usage /jenkins show [name]")
    else:
        if j.has_job(jobname):
            prof.cons_show("")
            job = j.get_job(jobname)
            prof.cons_show(jobname + " details:");

            desc = job.get_description()
            if desc:
                prof.cons_show  ("  Description : " + desc)

            if job.is_queued():
                prof.cons_show  ("  Status      : Queued")
            elif job.is_running():
                prof.cons_show  ("  Status      : Running")
            else:
                build = job.get_last_build_or_none()
                if build:
                    prof.cons_show  ("  Last build  : #" + str(build.get_number()))
                    prof.cons_show  ("  Status      : " + build.get_status())
                else:
                    prof.cons_show  ("  Last build  : No builds")

            prof.cons_show      ("  Trigger     : " + job.get_build_triggerurl())
            prof.cons_show("")
        else:
            prof.cons_show("No such job " + jobname)

def _build_job(j, jobname):
    if not jobname:
        prof.cons_show("Usage /jenkins build [name]")
    else:
        if j.has_job(jobname):
            job = j.get_job(jobname)
            try:
                job.invoke(invoke_pre_check_delay=1)
            except Exception, e:
                prof.cons_show("Failed to trigger build: " + str(e))
        else:
            prof.cons_show("No such job " + jobname)

def _open_job(j, jobname):
    if not jobname:
        prof.cons_show("Usage /jenkins open [name]")
    else:
        if j.has_job(jobname):
            _open_job_url(jenkins_url + "/job/" + jobname)
        else:
            prof.cons_show("No such job " + jobname)

def _cmd_jenkins(cmd, jobname=None):
    try:
        j = Jenkins(jenkins_url, username, password)
    except Exception:
        prof.cons_show("Jenkins down")
    else:
        if cmd == "jobs":
            _list_jobs(j)
        elif cmd == "show":
            _show_job(j, jobname)
        elif cmd == "build":
            _build_job(j, jobname)
        elif cmd == "open":
            _open_job(j, jobname)
        else:
            prof.cons_show("Usage: /jenkins jobs|show|build|open [name]")

def _process_job(name, job):
    global failing
    global passing

    if not job.is_queued_or_running():
        build = job.get_last_build_or_none()
        if build:
            if build.get_status() == "FAILURE":
                if not name in failing:
                    prof.cons_show("Jenkins job: " + name + " #" + str(build.get_number()) + " BROKEN")
                    prof.notify(name + " broken", 5000, "Build failed")
                    failing.append(name)
                if name in passing:
                    passing.remove(name)
            else:
                if name in failing:
                    prof.cons_show("Jenkins job: " + name + " #" + str(build.get_number()) + " FIXED")
                    prof.notify(name + " fixed", 5000, "Build fixed")
                    failing.remove(name)
                if not name in passing:
                    passing.append(name)

def _poll_jobs():
    try:
        j = Jenkins(jenkins_url, username, password)
    except Exception:
        prof.cons_show("Jenkins down")
    else:
        for name, job in j.get_jobs():
            _process_job(name, job)

def prof_init(version, status):
    prof.register_timed(_poll_jobs, 30)
    prof.register_command("/jenkins", 1, 2, "/jenkins jobs|show|build|open [name]", "Do jenkins stuff.", "Do jenkins stuff.",
        _cmd_jenkins)
