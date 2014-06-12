"""
Manage jenkins jobs

Prerequisites:
The jenkinsapi module is required https://pypi.python.org/pypi/jenkinsapi
To install the module using pip:
    sudo pip install jenkinsapi

The plugin polls the jenkins server at 'jenkins_url' every 'jenkins_poll_interval' seconds.

The results are checked by profanity every 'prof_cb_interval'.
New failures are reported in the jenkins window, and a desktop notification is sent.

The 'prof_remind_interval' specifies the time between reminder notifications of broken builds

"""

import prof
import os
import threading
import time
import webbrowser
import urllib2
import jenkinsapi
from jenkinsapi.jenkins import Jenkins

jenkins_url = "http://localhost:8080"
username = None
password = None

jenkins_poll_interval = 5
prof_cb_interval = 5
prof_remind_interval = 10
enable_notify = True
enable_remind = True

last_state = {}
STATE_SUCCESS = "SUCCESS"
STATE_UNSTABLE = "UNSTABLE"
STATE_FAILURE = "FAILURE"
STATE_QUEUED = "QUEUED"
STATE_RUNNING = "RUNNING"
STATE_NOBUILDS = "NOBUILDS"
STATE_UNKNOWN = "UNKNOWN" 

win_tag = "Jenkins"

poll_fail = False
poll_fail_message = None

job_list = None
changes_list = None

def _help():
    prof.win_show(win_tag, "Commands:")
    prof.win_show(win_tag, " /jenkins help - Show this help")
    prof.win_show(win_tag, " /jenkins jobs - List all jobs")
    prof.win_show(win_tag, " /jenkins failing - List all failing jobs")
    prof.win_show(win_tag, " /jenkins passing - List all passing jobs")
    prof.win_show(win_tag, " /jenkins unstable - List all unstable jobs")
    prof.win_show(win_tag, " /jenkins build [job] - Trigger build for job")
    prof.win_show(win_tag, " /jenkins open [job] - Open job in browser")
    prof.win_show(win_tag, " /jenkins log [job] - Show the latest build log")
    prof.win_show(win_tag, " /jenkins remind on|off - Enable/disable reminder notifications")
    prof.win_show(win_tag, " /jenkins notify on|off - Enable/disable build notifications")
    prof.win_show(win_tag, " /jenkins settings - Show current settings")

def _settings():
    prof.win_show(win_tag, "Jenkins settings:")
    prof.win_show(win_tag, "  Jenkins URL               : " + jenkins_url)
    prof.win_show(win_tag, "  Jenkins poll interval     : " + str(jenkins_poll_interval) + " seconds")
    prof.win_show(win_tag, "  Profanity update interval : " + str(prof_cb_interval) + " seconds")
    prof.win_show(win_tag, "  Reminder interval         : " + str(prof_remind_interval) + " seconds")
    prof.win_show(win_tag, "  Notifications enabled     : " + str(enable_notify))
    prof.win_show(win_tag, "  Reminders enabled         : " + str(enable_remind))

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

class JobList():
    def __init__(self):
        self.jobs = []

    def add_job(self, name, build_number, state):
        self.jobs.append((name, build_number, state))

    def get_jobs(self, in_state=None):
        if not in_state:
            return self.jobs
        else:
            result = []
            for name, build_number, state in self.jobs:
                if state == in_state:
                    result.append((name, build_number, state))
            return result

    def get_job(self, jobname):
        for name, build_number, state in self.jobs:
            if name == jobname:
                return name, build_number
        return None

    def contains_job(self, jobname):
        for name, build_number, state in self.jobs:
            if name == jobname:
                return True
        return False

    def num_in_state(self, given_state):
        count = 0
        for name, build_number, state in self.jobs:
            if state == given_state:
                count = count + 1
        return count

class JobUpdates():
    def __init__(self):
        self.states = {}
        self.states[STATE_FAILURE] = []
        self.states[STATE_SUCCESS] = []
        self.states[STATE_UNSTABLE] = []
        self.states[STATE_QUEUED] = []
        self.states[STATE_RUNNING] = []

    def add_update(self, state, name, build_number=None):
        if build_number:
            self.states[state].append((name, build_number))
        else:
            self.states[state].append(name)

    def get_in_state(self, state):
        return self.states[state]

def _process_build(name, build, new_job_list, new_changes_list):
    if build.get_status() == STATE_FAILURE:
        new_job_list.add_job(name, build.get_number(), STATE_FAILURE)
        changed = _set_state(name, STATE_FAILURE)
        if changed:
            new_changes_list.add_update(STATE_FAILURE, name, build.get_number())
    elif build.get_status() == STATE_SUCCESS:
        new_job_list.add_job(name, build.get_number(), STATE_SUCCESS)
        changed = _set_state(name, STATE_SUCCESS)
        if changed:
            new_changes_list.add_update(STATE_SUCCESS, name, build.get_number())
    elif build.get_status() == STATE_UNSTABLE:
        new_job_list.add_job(name, build.get_number(), STATE_UNSTABLE)
        changed = _set_state(name, STATE_UNSTABLE)
        if changed:
            new_changes_list.add_update(STATE_UNSTABLE, name, build.get_number())

def _process_queued_or_running(name, job, new_job_list, new_changes_list):
    if job.is_queued():
        new_job_list.add_job(name, None, STATE_QUEUED)
        changed = _set_state(name, STATE_QUEUED)
        if changed:
            new_changes_list.add_update(STATE_QUEUED, name)
    elif job.is_running():
        new_job_list.add_job(name, None, STATE_RUNNING)
        changed = _set_state(name, STATE_RUNNING)
        if changed:
            new_changes_list.add_update(STATE_RUNNING, name)

def _jenkins_poll():
    global poll_fail
    global poll_fail_message
    global job_list
    global changes_list

    job_ac = []

    while True:
        time.sleep(jenkins_poll_interval)
        try:
            j = Jenkins(jenkins_url, username, password)
        except Exception, e:
            poll_fail = True
            poll_fail_message = str(e)
        else:
            poll_fail = False
            poll_fail_message = None
            new_job_list = JobList()
            new_changes_list = JobUpdates()        
            for name, job in j.get_jobs():
                if not job.is_queued_or_running():
                    build = job.get_last_build_or_none()
                    if build:
                        _process_build(name, build, new_job_list, new_changes_list)
                    else:
                        new_job_list.add_job(name, None, STATE_NOBUILDS)
                else:
                    _process_queued_or_running(name, job, new_job_list, new_changes_list)
                if not job_list:
                    job_ac.append(name)

            if not job_list:
                prof.register_ac("/jenkins build", job_ac)
                prof.register_ac("/jenkins open", job_ac)
                prof.register_ac("/jenkins log", job_ac)

            job_list = new_job_list
            changes_list = new_changes_list

def _prof_callback():
    global changes_list
    if poll_fail:
        if not prof.win_exists(win_tag):
            prof.win_create(win_tag, _handle_input)
        prof.win_show(win_tag, "Could not connect to jenkins, see the logs.")
        if poll_fail_message:
            prof.log_warning("Jenkins poll failed: " + str(poll_fail_message))
        else:
            prof.log_warning("Jenkins poll failed")
    elif changes_list:
        for name in changes_list.get_in_state(STATE_QUEUED):
            if not prof.win_exists(win_tag):
                prof.win_create(win_tag, _handle_input)
            prof.win_show_cyan(win_tag, name + " " + STATE_QUEUED)
        for name in changes_list.get_in_state(STATE_RUNNING):
            if not prof.win_exists(win_tag):
                prof.win_create(win_tag, _handle_input)
            prof.win_show_cyan(win_tag, name + " " + STATE_RUNNING)
        for name, build_number in changes_list.get_in_state(STATE_SUCCESS):
            if not prof.win_exists(win_tag):
                prof.win_create(win_tag, _handle_input)
            prof.win_show_green(win_tag, name + " #" + str(build_number) + " " + STATE_SUCCESS)
            if enable_notify:
                prof.notify(name + " " + STATE_SUCCESS, 5000, "Jenkins")
        for name, build_number in changes_list.get_in_state(STATE_UNSTABLE):
            if not prof.win_exists(win_tag):
                prof.win_create(win_tag, _handle_input)
            prof.win_show_yellow(win_tag, name + " #" + str(build_number) + " " + STATE_UNSTABLE)
            if enable_notify:
                prof.notify(name + " " + STATE_UNSTABLE, 5000, "Jenkins")
        for name, build_number in changes_list.get_in_state(STATE_FAILURE):
            if not prof.win_exists(win_tag):
                prof.win_create(win_tag, _handle_input)
            prof.win_show_red(win_tag, name + " #" + str(build_number) + " " + STATE_FAILURE)
            if enable_notify:
                prof.notify(name + " " + STATE_FAILURE, 5000, "Jenkins")

        changes_list = None

def _handle_input(win, line):
    pass

def _list_jobs(jobs):
    for name, build_number, state in jobs:
        if state == STATE_SUCCESS:
            prof.win_show_green(win_tag, "  " + name + " #" + str(build_number) + " " + STATE_SUCCESS)
        elif state == STATE_UNSTABLE:
            prof.win_show_yellow(win_tag, "  " + name + " #" + str(build_number) + " " + STATE_UNSTABLE)
        elif state == STATE_FAILURE:
            prof.win_show_red(win_tag, "  " + name + " #" + str(build_number) + " " + STATE_FAILURE)
        elif state == STATE_NOBUILDS:
            prof.win_show(win_tag, "  " + name + ", no builds")
        else:
            prof.win_show_cyan(win_tag, "  " + name + " " + state)

def _build_job(job):
    try:
        urllib2.urlopen(jenkins_url + "/job/" + job + "/build")
    except Exception, e:
        prof.win_show(win_tag, "Failed to build " + job + ", see the logs.")
        prof.log_warning("Failed to build " + job + ": " + str(e))
    else:
        prof.win_show(win_tag, "Build request sent for " + job)

def _job_log(job):
    name = job[0]
    build_no = job[1]
    if build_no:
        try:
            response = urllib2.urlopen(jenkins_url + "/job/" + name + "/" + str(build_no) + "/consoleText")
        except Exception, e:
            prof.win_show(win_tag, "Unable to fetch log for " + name + "#" + str(build_no) + ", see the logs.")
            prof.log_warning("Unable to fetch log for " + name + "#" + str(build_no) + ": " + str(e))
        else:
            log_str = "Log for " + name + " #" + str(build_no) + ":\n" + response.read()
            prof.win_show(win_tag, log_str)
    else:
        prof.win_show(win_tag, "No build found for " + name)

def _cmd_jenkins(cmd=None, arg=None):
    global enable_remind
    global enable_notify

    if not prof.win_exists(win_tag):
        prof.win_create(win_tag, _handle_input)

    prof.win_focus(win_tag)

    if cmd == "jobs":
        if job_list and job_list.get_jobs():
            prof.win_show(win_tag, "Jobs:")
            _list_jobs(job_list.get_jobs())
        else:
            prof.win_show(win_tag, "No job data yet.")
    elif cmd == "failing":
        if job_list:
            jobs_in_state = job_list.get_jobs(STATE_FAILURE)
            if jobs_in_state:
                prof.win_show(win_tag, "Failing jobs:")
                _list_jobs(jobs_in_state)
            else:
                prof.win_show(win_tag, "No failing jobs.")
        else:
            prof.win_show(win_tag, "No job data yet.")
    elif cmd == "passing":
        if job_list:
            jobs_in_state = job_list.get_jobs(STATE_SUCCESS)
            if jobs_in_state:
                prof.win_show(win_tag, "Passing jobs:")
                _list_jobs(jobs_in_state)
            else:
                prof.win_show(win_tag, "No passing jobs.")
        else:
            prof.win_show(win_tag, "No job data yet.")
    elif cmd == "unstable":
        if job_list:
            jobs_in_state = job_list.get_jobs(STATE_UNSTABLE)
            if jobs_in_state:
                prof.win_show(win_tag, "Unstable jobs:")
                _list_jobs(jobs_in_state)
            else:
                prof.win_show(win_tag, "No unstable jobs.")
        else:
            prof.win_show(win_tag, "No job data yet.")
    elif cmd == "build":
        if not arg:
            prof.win_show(win_tag, "You must supply a job argument.")
        elif job_list and job_list.contains_job(arg):
            _build_job(arg)
        else:
            prof.win_show(win_tag, "No such job: " + arg)
    elif cmd == "open":
        if not arg:
            prof.win_show(win_tag, "You must supply a job argument.")
        elif job_list and job_list.contains_job(arg):
            _open_job_url(jenkins_url + "/job/" + arg)
        else:
            prof.win_show(win_tag, "No such job: " + arg)
    elif cmd == "remind":
        if not arg:
            prof.win_show(win_tag, "You must specify either 'on' or 'off'.")
        elif arg == "on":
            enable_remind = True
            prof.win_show(win_tag, "Reminder notifications enabled.")
        elif arg == "off":
            enable_remind = False
            prof.win_show(win_tag, "Reminder notifications disabled.")
        else:
            prof.win_show(win_tag, "You must specify either 'on' or 'off'.")
    elif cmd == "notify":
        if not arg:
            prof.win_show(win_tag, "You must specify either 'on' or 'off'.")
        elif arg == "on":
            enable_notify = True
            prof.win_show(win_tag, "Build notifications enabled.")
        elif arg == "off":
            enable_notify = False
            prof.win_show(win_tag, "Build notifications disabled.")
        else:
            prof.win_show(win_tag, "You must specify either 'on' or 'off'.")
    elif cmd == "settings":
        _settings()
    elif cmd == "help":
        _help()
    elif cmd == "log":
        if not arg:
            prof.win_show(win_tag, "You must specify a job.")
        else:
            job = job_list.get_job(arg)
            if job:
                _job_log(job)
            else:
                prof.win_show(win_tag, "No job found: " + arg)
    else:
        prof.win_show(win_tag, "Unknown command.")

def _remind():
    if enable_remind and job_list:
        notify_string = ""
        failing = job_list.num_in_state(STATE_FAILURE)
        unstable = job_list.num_in_state(STATE_UNSTABLE)

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

def prof_init(version, status):
    last_state[STATE_SUCCESS] = []
    last_state[STATE_UNSTABLE] = []
    last_state[STATE_FAILURE] = []
    last_state[STATE_QUEUED] = []
    last_state[STATE_RUNNING] = []
    last_state[STATE_NOBUILDS] = []
    last_state[STATE_UNKNOWN] = []

    jenkins_t = threading.Thread(target=_jenkins_poll)
    jenkins_t.daemon = True;
    jenkins_t.start()

    prof.register_timed(_prof_callback, prof_cb_interval)
    prof.register_timed(_remind, prof_remind_interval)

    cmd_ac = [ "help", "jobs", "failing", "passing", "unstable", "build", "open", "log", "remind", "notify", "settings" ]
    prof.register_ac("/jenkins", cmd_ac);
    remind_ac = [ "on", "off" ]
    prof.register_ac("/jenkins remind", remind_ac);
    notify_ac = [ "on", "off" ]
    prof.register_ac("/jenkins notify", notify_ac);
    prof.register_command("/jenkins", 0, 2, "/jenkins list|build|open|remind|notify|settings|help", "Do jenkins stuff.", "Do jenkins stuff.",
        _cmd_jenkins)

def prof_on_start():
    prof.win_create(win_tag, _handle_input)
    prof.win_show(win_tag, "Jenkins plugin started.")
