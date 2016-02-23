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
            prof_cons_bad_cmd_usage("/c-test");
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
            prof_cons_bad_cmd_usage("/c-test");
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
            prof_cons_bad_cmd_usage("/c-test");
        }
    } else if (strcmp(args[0], "get") == 0) {
        if (!args[1]) {
            prof_cons_bad_cmd_usage("/c-test");
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
            prof_cons_bad_cmd_usage("/c-test");
        }
    } else if (strcmp(args[0], "log") == 0) {
        if (!args[1]) {
            prof_cons_bad_cmd_usage("/c-test");
        } else if (strcmp(args[1], "debug") == 0) {
            if (!args[2]) {
                prof_cons_bad_cmd_usage("/c-test");
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
                prof_cons_bad_cmd_usage("/c-test");
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
                prof_cons_bad_cmd_usage("/c-test");
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
                prof_cons_bad_cmd_usage("/c-test");
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
            prof_cons_bad_cmd_usage("/c-test");
        }
    } else {
        prof_cons_bad_cmd_usage("/c-test");
    }
}

void
prof_init(const char * const version, const char * const status)
{
    prof_win_create(plugin_win, handle_win_input);

/* TODO ADD COMMAND

    prof_cons_show_themed("c-test", "test.out", NULL, "This from test.out");
    prof_cons_show_themed("c-test", "another.theme", "yellow", "This from another.theme, default yellow");
    prof_cons_show_themed("c-test", "more.theme", "bold_cyan", "This from more.theme, default bold cyan");
    prof_cons_show_themed(NULL, NULL, "white", "This is white");
    prof_cons_show_themed(NULL, NULL, "bold_white", "This is bold white");
    prof_cons_show_themed(NULL, NULL, "red", "This is red");
    prof_cons_show_themed(NULL, NULL, "bold_red", "This is bold red");
    prof_cons_show_themed(NULL, NULL, "green", "This is green");
    prof_cons_show_themed(NULL, NULL, "bold_green", "This is bold green");
    prof_cons_show_themed(NULL, NULL, "blue", "This is blue");
    prof_cons_show_themed(NULL, NULL, "bold_blue", "This is bold blue");
    prof_cons_show_themed(NULL, NULL, "yellow", "This is yellow");
    prof_cons_show_themed(NULL, NULL, "bold_yellow", "This is bold yellow");
    prof_cons_show_themed(NULL, NULL, "cyan", "This is cyan");
    prof_cons_show_themed(NULL, NULL, "bold_cyan", "This is bold cyan");
    prof_cons_show_themed(NULL, NULL, "magenta", "This is magenta");
    prof_cons_show_themed(NULL, NULL, "bold_magenta", "This is bold magenta");
    prof_cons_show_themed(NULL, NULL, "black", "This is black");
    prof_cons_show_themed(NULL, NULL, "bold_black", "This is bold_black");

    prof_win_show_themed(plugin_win, "c-test", "test.out", NULL, "This from test.out");
    prof_win_show_themed(plugin_win, "c-test", "another.theme", "yellow", "This from another.theme, default yellow");
    prof_win_show_themed(plugin_win, "c-test", "more.theme", "bold_cyan", "This from more.theme, default bold cyan");
    prof_win_show_themed(plugin_win, NULL, NULL, "white", "This is white");
    prof_win_show_themed(plugin_win, NULL, NULL, "bold_white", "This is bold white");
    prof_win_show_themed(plugin_win, NULL, NULL, "red", "This is red");
    prof_win_show_themed(plugin_win, NULL, NULL, "bold_red", "This is bold red");
    prof_win_show_themed(plugin_win, NULL, NULL, "green", "This is green");
    prof_win_show_themed(plugin_win, NULL, NULL, "bold_green", "This is bold green");
    prof_win_show_themed(plugin_win, NULL, NULL, "blue", "This is blue");
    prof_win_show_themed(plugin_win, NULL, NULL, "bold_blue", "This is bold blue");
    prof_win_show_themed(plugin_win, NULL, NULL, "yellow", "This is yellow");
    prof_win_show_themed(plugin_win, NULL, NULL, "bold_yellow", "This is bold yellow");
    prof_win_show_themed(plugin_win, NULL, NULL, "cyan", "This is cyan");
    prof_win_show_themed(plugin_win, NULL, NULL, "bold_cyan", "This is bold cyan");
    prof_win_show_themed(plugin_win, NULL, NULL, "magenta", "This is magenta");
    prof_win_show_themed(plugin_win, NULL, NULL, "bold_magenta", "This is bold magenta");
    prof_win_show_themed(plugin_win, NULL, NULL, "black", "This is black");
    prof_win_show_themed(plugin_win, NULL, NULL, "bold_black", "This is bold_black");

*/

    const char *synopsis[] = {
        "/c-test consalert",
        "/c-test consshow <message>",
        "/c-test notify <message>",
        "/c-test sendline <line>",
        "/c-test get recipient|room",
        "/c-test log debug|info|warning|error <message>",
        NULL
    };
    const char *description = "C test plugin. All commands focus the plugin window.";
    const char *args[][2] = {
        { "consalert",                              "Highlight the console window in the status bar" },
        { "consshow <message>",                     "Show the message in the console window" },
        { "notify <message>",                       "Send a desktop notification with message" },
        { "sendline <line>",                        "Pass line to profanity to process" },
        { "get recipient",                          "Show the current chat recipient, if in a chat window" },
        { "get room",                               "Show the current room JID, if in a chat room" },
        { "log debug|info|warning|error <message>", "Log a message at the specified level" },
        { NULL, NULL }
    };

    const char *examples[] = {
        "/c-test sendline /about",
        "/c-test log debug \"Test debug message\"",
        NULL
    };

    prof_register_command("/c-test", 1, 3, synopsis, description, args, examples, cmd_ctest);

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
