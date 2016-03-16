/*
Simple plugin to display the PID of the Profanity process and its parent
 
Theme example in ~/.local/share/profanity/plugin_themes

[pid]
self=bold_white
parent=white
*/

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

#include <profapi.h>

void
cmd_pid(char **args)
{
    pid_t pid = getpid();
    pid_t ppid = getppid();
    char buf[50];
    sprintf(buf, "PID: %d", pid);
    prof_cons_show_themed("pid", "self", NULL, buf);
    sprintf(buf, "Parent PID: %d", ppid);
    prof_cons_show_themed("pid", "parent", NULL, buf);
    prof_cons_alert();
}

void
prof_init(const char * const version, const char * const status)
{
    const char *synopsis[] = { "/pid", NULL };
    const char *description = "Show process ID and parent Process ID in the console window.";
    const char *args[][2] = { { NULL, NULL } };
    const char *examples[] = { NULL };

    prof_register_command("/pid", 0, 0, synopsis, description, args, examples, cmd_pid);
}
