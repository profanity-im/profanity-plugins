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
    sprintf(buf, "PID: %d, parent PID: %d", pid, ppid);
    prof_cons_show(buf);
    prof_cons_alert();
}

void
prof_init(const char * const version, const char * const status)
{
    prof_register_command("/pid", 0, 0, "/pid", "Get process ID", "Get process ID", cmd_pid);
}
