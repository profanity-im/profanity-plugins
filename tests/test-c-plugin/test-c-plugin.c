#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <ctype.h>

#include <profapi.h>

static PROF_WIN_TAG echo_win = "Reverse Echo";

void
timer_test(void)
{
    prof_cons_show("c-test: timer fired.");
    char *recipient = prof_get_current_recipient();
    if (recipient != NULL) {
        char *start = "  current recipient = ";
        char buf[strlen(start) + strlen(recipient) + 1];
        sprintf(buf, "%s%s", start, recipient);
        prof_cons_show(buf);
    }
    prof_cons_alert();
}

char*
convert_to_upper(char *str) {
    char *newstr = strdup(str);
    char *p = newstr;
    
    while (*p != '\0') {
        *p = toupper(*p);
        p++;
    }

    return newstr;
}

void
handle_upper(PROF_WIN_TAG win, char *line)
{
    char *upper = convert_to_upper(line);
    prof_win_show(win, upper);

    char buf[strlen(upper) + 8];
    sprintf(buf, "%s %s", upper, "red");
    prof_win_show_red(win, buf);
    sprintf(buf, "%s %s", upper, "yellow");
    prof_win_show_yellow(win, buf);
    sprintf(buf, "%s %s", upper, "green");
    prof_win_show_green(win, buf);
    sprintf(buf, "%s %s", upper, "cyan");
    prof_win_show_cyan(win, buf);

    free(upper);
}

void
cmd_c(char **args)
{
    if (args[0] != NULL) {
        char *start = "c-test: /c command called, arg = ";
        char buf[strlen(start) + strlen(args[0]) + 1];
        sprintf(buf, "%s%s", start, args[0]);
        prof_cons_show(buf);
    } else {
        prof_cons_show("c-test: /c command called with no arg");
    }
}

void
cmd_ac(char **args) {
    prof_cons_show("c-test: /c_complete called");
}

void
cmd_upper(char **args)
{
    if (!prof_win_exists(echo_win)) {
        prof_win_create(echo_win, handle_upper);
    }

    prof_win_focus(echo_win);
    if (args[0] != NULL) {
        handle_upper(echo_win, args[0]);
    }
}

void
cmd_notification(char **args) {
    prof_notify("c-test: notify", 2000, "Plugins");
}

void
cmd_verchecker(char **args) {
    prof_send_line("/vercheck");
    prof_cons_show("c-test: sent \"/vercheck\" command");
}

void
prof_init(const char * const version, const char * const status)
{
    char *start = "c-test: init. ";
    char buf[strlen(start) + strlen(version) + 2 + strlen(status) + 1];
    sprintf(buf, "%s%s, %s", start, version, status);
    prof_cons_show(buf);
    prof_register_command("/c", 0, 1, "/c [arg]", "c test", "c test", cmd_c);
    prof_register_command("/c_upper", 1, 1, "/c_upper", "c test", "c test", cmd_upper);
    prof_register_command("/c_notify", 0, 0, "/c_notify", "c test", "c test", cmd_notification);
    prof_register_command("/c_vercheck", 0, 0, "/c_vercheck", "c test", "c test", cmd_verchecker);
    char *arg1_ac[] = { "aaaa", "bbbb", "bcbcbc", NULL };
    char *arg2_ac1[] = { "one", "two", "three", "four", NULL };
    char *arg1_ac2[] = { "james", "jim", "jane", "bob", NULL };
    prof_register_ac("/c_complete", arg1_ac);
    prof_register_ac("/c_complete aaaa", arg2_ac1);
    prof_register_ac("/c_complete bcbcbc", arg1_ac2);
    prof_register_command("/c_complete", 0, 2, "/c_complete [arg1] [arg2]", "c test", "c test", cmd_ac);
    prof_register_timed(timer_test, 30);
}

void
prof_on_start(void)
{
    prof_cons_show("c-test: prof_on_start");
    prof_log_debug("c-test: logged debug");
    prof_log_info("c-test: logged info");
    prof_log_warning("c-test: logged warning");
    prof_log_error("c-test: logged error");
}

void
prof_on_shutdown(void)
{
    prof_log_info("c-test: prof_on_shutdown");
}

void
prof_on_connect(const char * const account_name, const char * const fulljid)
{
    char *start = "c-test: prof_on_connect, ";
    char buf[strlen(start) + strlen(account_name) + 2 + strlen(fulljid) + 1];
    sprintf(buf, "%s%s, %s", start, account_name, fulljid);
    prof_cons_show(buf);
}

void
prof_on_disconnect(const char * const account_name, const char * const fulljid)
{
    char *start = "c-test: prof_on_disconnect, ";
    char buf[strlen(start) + strlen(account_name) + 2 + strlen(fulljid) + 1];
    sprintf(buf, "%s%s, %s", start, account_name, fulljid);
    prof_cons_show(buf);
    prof_log_info(buf);
}

char *
prof_pre_chat_message_display(const char * const jid, const char *message)
{
    char *start = "c-test: prof_pre_chat_message_display, ";
    char buf[strlen(start) + strlen(jid) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s", start, jid, message);
    prof_cons_show(buf);
    prof_cons_alert();
    char *result = malloc(strlen(message) + 29);
    sprintf(result, "%s%s", message, "[C_pre_chat_message_display]");

    return result;
}

void
prof_post_chat_message_display(const char * const jid, const char *message)
{
    char *start = "c-test: prof_post_chat_message_display, ";
    char buf[strlen(start) + strlen(jid) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s", start, jid, message);
    prof_cons_show(buf);
    prof_cons_alert();
}

char *
prof_pre_chat_message_send(const char * const jid, const char *message)
{
    char *start = "c-test: prof_pre_chat_message_send, ";
    char buf[strlen(start) + strlen(jid) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s", start, jid, message);
    prof_cons_show(buf);
    prof_cons_alert();
    char *result = malloc(strlen(message) + 26);
    sprintf(result, "%s%s", message, "[C_pre_chat_message_send]");

    return result;
}

void
prof_post_chat_message_send(const char * const jid, const char *message)
{
    char *start = "c-test: prof_post_chat_message_send, ";
    char buf[strlen(start) + strlen(jid) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s", start, jid, message);
    prof_cons_show(buf);
    prof_cons_alert();
}

char *
prof_pre_room_message_display(const char * const room, const char * const nick, const char *message)
{
    char *start = "c-test: prof_pre_room_message_display, ";
    char buf[strlen(start) + strlen(room) + 2 + strlen(nick) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s, %s", start, room, nick, message);
    prof_cons_show(buf);
    prof_cons_alert();
    char *result = malloc(strlen(message) + 29);
    sprintf(result, "%s%s", message, "[C_pre_room_message_display]");

    return result;
}

void
prof_post_room_message_display(const char * const room, const char * const nick, const char *message)
{
    char *start = "c-test: prof_post_room_message_display, ";
    char buf[strlen(start) + strlen(room) + 2 + strlen(nick) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s, %s", start, room, nick, message);
    prof_cons_show(buf);
    prof_cons_alert();
}

char *
prof_pre_room_message_send(const char * const room, const char *message)
{
    char *start = "c-test: prof_pre_room_message_display, ";
    char buf[strlen(start) + strlen(room) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s", start, room, message);
    prof_cons_show(buf);
    prof_cons_alert();
    char *result = malloc(strlen(message) + 26);
    sprintf(result, "%s%s", message, "[C_pre_room_message_send]");

    return result;
}

void
prof_post_room_message_send(const char * const room, const char *message)
{
    char *start = "c-test: prof_post_room_message_display, ";
    char buf[strlen(start) + strlen(room) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s", start, room, message);
    prof_cons_show(buf);
    prof_cons_alert();
}

char *
prof_pre_priv_message_display(const char * const room, const char * const nick, const char *message)
{
    char *start = "c-test: prof_pre_priv_message_display, ";
    char buf[strlen(start) + strlen(room) + 2 + strlen(nick) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s, %s", start, room, nick, message);
    prof_cons_show(buf);
    prof_cons_alert();
    char *result = malloc(strlen(message) + 29);
    sprintf(result, "%s%s", message, "[C_pre_priv_message_display]");

    return result;
}

void
prof_post_priv_message_display(const char * const room, const char * const nick, const char *message)
{
    char *start = "c-test: prof_post_priv_message_display, ";
    char buf[strlen(start) + strlen(room) + 2 + strlen(nick) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s, %s", start, room, nick, message);
    prof_cons_show(buf);
    prof_cons_alert();
}

char *
prof_pre_priv_message_send(const char * const room, const char * const nick, const char *message)
{
    char *start = "c-test: prof_pre_priv_message_send, ";
    char buf[strlen(start) + strlen(room) + 2 + strlen(nick) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s, %s", start, room, nick, message);
    prof_cons_show(buf);
    prof_cons_alert();
    char *result = malloc(strlen(message) + 26);
    sprintf(result, "%s%s", message, "[C_pre_priv_message_send]");

    return result;
}

void
prof_post_priv_message_send(const char * const room, const char * const nick, const char *message)
{
    char *start = "c-test: prof_post_priv_message_send, ";
    char buf[strlen(start) + strlen(room) + 2 + strlen(nick) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s, %s", start, room, nick, message);
    prof_cons_show(buf);
    prof_cons_alert();
}