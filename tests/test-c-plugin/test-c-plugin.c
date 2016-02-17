#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <ctype.h>

#include <profapi.h>

static PROF_WIN_TAG plugin_win = "C Test";

void
handle_win_input(PROF_WIN_TAG win, char *line)
{
    char *str = "Input received: ";
    char buf[strlen(str) + strlen(line) + 1];
    sprintf(buf, "%s%s", str, line);
    prof_win_show(win, buf);
}

void create_win(void)
{
    if (!prof_win_exists(plugin_win)) {
        prof_win_create(plugin_win, handle_win_input);
    }
}

void
cmd_ctest(char **args)
{
    if (strcmp(args[0], "consalert") == 0) {
        create_win();
        prof_win_focus(plugin_win);
        prof_cons_alert();
        prof_win_show(plugin_win, "called -> prof_cons_alert");
    } else if (strcmp(args[0], "consshow") == 0) {
        if (args[1]) {
            create_win();
            prof_win_focus(plugin_win);
            prof_cons_show(args[1]);
            char *str = "called -> prof_cons_show: ";
            char buf[strlen(str) + strlen(args[1])];
            sprintf(buf, "%s%s", str, args[1]);
            prof_win_show(plugin_win, buf);
        } else {
            prof_cons_show("Invalid usage, see '/help c-test' for details.");
        }
    } else if (strcmp(args[0], "sendline") == 0) {
        if (args[1]) {
            create_win();
            prof_win_focus(plugin_win);
            prof_send_line(args[1]);
            char *str = "called -> prof_send_line: ";
            char buf[strlen(str) + strlen(args[1])];
            sprintf(buf, "%s%s", str, args[1]);
            prof_win_show(plugin_win, buf);
        } else {
            prof_cons_show("Invalid usage, see '/help c-test' for details.");
        }
    } else if (strcmp(args[0], "notify") == 0) {
        if (args[1]) {
            create_win();
            prof_win_focus(plugin_win);
            prof_notify(args[1], 5000, "c-test plugin");
            char *str = "called -> prof_notify: ";
            char buf[strlen(str) + strlen(args[1])];
            sprintf(buf, "%s%s", str, args[1]);
            prof_win_show(plugin_win, buf);
        } else {
            prof_cons_show("Invalid usage, see '/help c-test' for details.");
        }
    } else if (strcmp(args[0], "get") == 0) {
        if (!args[1]) {
            prof_cons_show("Invalid usage, see '/help c-test' for details.");
        } else if (strcmp(args[1], "recipient") == 0) {
            create_win();
            char *recipient = prof_get_current_recipient();
            if (recipient) {
                prof_win_focus(plugin_win);
                char *str = "called -> prof_get_current_recipient: ";
                char buf[strlen(str) + strlen(recipient)];
                sprintf(buf, "%s%s", str, recipient);
                prof_win_show(plugin_win, buf);
            } else {
                prof_win_focus(plugin_win);
                prof_win_show(plugin_win, "called -> prof_get_current_recipient: <none>");
            }
        } else if (strcmp(args[1], "room") == 0) {
            create_win();
            char *room = prof_get_current_muc();
            if (room) {
                prof_win_focus(plugin_win);
                char *str = "called -> prof_get_current_muc: ";
                char buf[strlen(str) + strlen(room)];
                sprintf(buf, "%s%s", str, room);
                prof_win_show(plugin_win, buf);
            } else {
                prof_win_focus(plugin_win);
                prof_win_show(plugin_win, "called -> prof_get_current_muc: <none>");
            }
        } else {
            prof_cons_show("Invalid usage, see '/help c-test' for details.");
        }
    } else if (strcmp(args[0], "log") == 0) {
        if (!args[1]) {
            prof_cons_show("Invalid usage, see '/help c-test' for details.");
        } else if (strcmp(args[1], "debug") == 0) {
            if (!args[2]) {
                prof_cons_show("Invalid usage, see '/help c-test' for details.");
            } else {
                create_win();
                prof_win_focus(plugin_win);
                prof_log_debug(args[2]);
                char *str = "called -> prof_log_debug: ";
                char buf[strlen(str) + strlen(args[2])];
                sprintf(buf, "%s%s", str, args[2]);
                prof_win_show(plugin_win, buf);
            }
        } else if (strcmp(args[1], "info") == 0) {
            if (!args[2]) {
                prof_cons_show("Invalid usage, see '/help c-test' for details.");
            } else {
                create_win();
                prof_win_focus(plugin_win);
                prof_log_info(args[2]);
                char *str = "called -> prof_log_info: ";
                char buf[strlen(str) + strlen(args[2])];
                sprintf(buf, "%s%s", str, args[2]);
                prof_win_show(plugin_win, buf);
            }
        } else if (strcmp(args[1], "warning") == 0) {
            if (!args[2]) {
                prof_cons_show("Invalid usage, see '/help c-test' for details.");
            } else {
                create_win();
                prof_win_focus(plugin_win);
                prof_log_warning(args[2]);
                char *str = "called -> prof_log_warning: ";
                char buf[strlen(str) + strlen(args[2])];
                sprintf(buf, "%s%s", str, args[2]);
                prof_win_show(plugin_win, buf);
            }
        } else if (strcmp(args[1], "error") == 0) {
            if (!args[2]) {
                prof_cons_show("Invalid usage, see '/help c-test' for details.");
            } else {
                create_win();
                prof_win_focus(plugin_win);
                prof_log_error(args[2]);
                char *str = "called -> prof_log_error: ";
                char buf[strlen(str) + strlen(args[2])];
                sprintf(buf, "%s%s", str, args[2]);
                prof_win_show(plugin_win, buf);
            }
        } else {
            prof_cons_show("Invalid usage, see '/help c-test' for details.");
        }
    } else {
        prof_cons_show("Invalid usage, see '/help c-test' for details.");
    }
}

void
prof_init(const char * const version, const char * const status)
{
    prof_win_create(plugin_win, handle_win_input);
    prof_register_command("/c-test", 1, 3, "/c-test", "C Test plugin", "C Test plugin", cmd_ctest);
    char *cmd_ac[] = { "consalert", "consshow", "notify", "sendline", "get", "log", NULL };
    prof_register_ac("/c-test", cmd_ac);
    char *get_ac[] = { "recipient", "room", NULL };
    prof_register_ac("/c-test get", get_ac);
    char *log_ac[] = { "debug", "info", "warning", "error", NULL };
    prof_register_ac("/c-test log", log_ac);
}

void
prof_on_start(void)
{
    create_win();
    prof_win_show(plugin_win, "fired -> prof_on_start");
}

void
prof_on_shutdown(void)
{
    create_win();
    prof_win_show(plugin_win, "fired -> prof_on_shutdown");
}

void
prof_on_connect(const char * const account_name, const char * const fulljid)
{
    create_win();

    char *str = "fired -> prof_on_connect: ";
    char buf[strlen(str) + strlen(account_name) + 2 + strlen(fulljid) + 1];
    sprintf(buf, "%s%s, %s", str, account_name, fulljid);
    prof_win_show(plugin_win, buf);
}

void
prof_on_disconnect(const char * const account_name, const char * const fulljid)
{
    create_win();

    char *str = "fired -> prof_on_disconnect: ";
    char buf[strlen(str) + strlen(account_name) + 2 + strlen(fulljid) + 1];
    sprintf(buf, "%s%s, %s", str, account_name, fulljid);
    prof_win_show(plugin_win, buf);
}

char*
prof_pre_chat_message_display(const char * const jid, const char *message)
{
    create_win();

    char *str = "fired -> prof_pre_chat_message_display: ";
    char buf[strlen(str) + strlen(jid) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s", str, jid, message);
    prof_win_show(plugin_win, buf);

    return NULL;
}

void
prof_post_chat_message_display(const char * const jid, const char *message)
{
    create_win();

    char *str = "fired -> prof_post_chat_message_display: ";
    char buf[strlen(str) + strlen(jid) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s", str, jid, message);
    prof_win_show(plugin_win, buf);
}

char*
prof_pre_chat_message_send(const char * const jid, const char *message)
{
    create_win();

    char *str = "fired -> prof_pre_chat_message_send: ";
    char buf[strlen(str) + strlen(jid) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s", str, jid, message);
    prof_win_show(plugin_win, buf);

    return NULL;
}

void
prof_post_chat_message_send(const char * const jid, const char *message)
{
    create_win();

    char *str = "fired -> prof_post_chat_message_send: ";
    char buf[strlen(str) + strlen(jid) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s", str, jid, message);
    prof_win_show(plugin_win, buf);
}

char*
prof_pre_room_message_display(const char * const room, const char * const nick, const char *message)
{
    create_win();

    char *str = "fired -> prof_pre_room_message_display: ";
    char buf[strlen(str) + strlen(room) + 2 + strlen(nick) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s, %s", str, room, nick, message);
    prof_win_show(plugin_win, buf);

    return NULL;
}

void
prof_post_room_message_display(const char * const room, const char * const nick, const char *message)
{
    create_win();

    char *str = "fired -> prof_post_room_message_display: ";
    char buf[strlen(str) + strlen(room) + 2 + strlen(nick) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s, %s", str, room, nick, message);
    prof_win_show(plugin_win, buf);
}

char *
prof_pre_room_message_send(const char * const room, const char *message)
{
    create_win();

    char *str = "fired -> prof_pre_room_message_send: ";
    char buf[strlen(str) + strlen(room) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s", str, room, message);
    prof_win_show(plugin_win, buf);

    return NULL;
}

void
prof_post_room_message_send(const char * const room, const char *message)
{
    create_win();

    char *str = "fired -> prof_post_room_message_send: ";
    char buf[strlen(str) + strlen(room) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s", str, room, message);
    prof_win_show(plugin_win, buf);
}

char *
prof_pre_priv_message_display(const char * const room, const char * const nick, const char *message)
{
    create_win();

    char *str = "fired -> prof_pre_priv_message_display: ";
    char buf[strlen(str) + strlen(room) + 2 + strlen(nick) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s, %s", str, room, nick, message);
    prof_win_show(plugin_win, buf);

    return NULL;
}

void
prof_post_priv_message_display(const char * const room, const char * const nick, const char *message)
{
    create_win();

    char *str = "fired -> prof_post_priv_message_display: ";
    char buf[strlen(str) + strlen(room) + 2 + strlen(nick) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s, %s", str, room, nick, message);
    prof_win_show(plugin_win, buf);
}

char *
prof_pre_priv_message_send(const char * const room, const char * const nick, const char *message)
{
    create_win();

    char *str = "fired -> prof_pre_priv_message_send: ";
    char buf[strlen(str) + strlen(room) + 2 + strlen(nick) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s, %s", str, room, nick, message);
    prof_win_show(plugin_win, buf);

    return NULL;
}

void
prof_post_priv_message_send(const char * const room, const char * const nick, const char *message)
{
    create_win();

    char *str = "fired -> prof_post_priv_message_send: ";
    char buf[strlen(str) + strlen(room) + 2 + strlen(nick) + 2 + strlen(message) + 1];
    sprintf(buf, "%s%s, %s, %s", str, room, nick, message);
    prof_win_show(plugin_win, buf);
}
