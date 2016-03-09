#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <ctype.h>
#include <pthread.h>
#include <unistd.h>

#include <profapi.h>

static PROF_WIN_TAG plugin_win = "C Test";
static pthread_t worker_thread;
static int count = 0;

void*
inc_counter(void *arg)
{
    while (1) {
        sleep(5);
        count++;
    }
}

void
handle_win_input(PROF_WIN_TAG win, char *line)
{
    char *str = "Input received: ";
    char buf[strlen(str) + strlen(line) + 1];
    sprintf(buf, "%s%s", str, line);
    prof_win_show(win, buf);
}

void
create_win(void)
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
    } else if (strcmp(args[0], "consshow_t") == 0) {
        if (args[1] == NULL || args[2] == NULL || args[3] == NULL || args[4] == NULL) {
            prof_cons_bad_cmd_usage("/c-test");
        } else {
            char *group = strcmp(args[1], "none") == 0 ? NULL : args[1];
            char *key = strcmp(args[2], "none") == 0 ? NULL : args[2];
            char *def = strcmp(args[3], "none") == 0 ? NULL : args[3];
            char *message = args[4];
            create_win();
            prof_win_focus(plugin_win);
            prof_cons_show_themed(group, key, def, message);
            char *str = "called -> prof_cons_show_themed: ";
            char buf[strlen(str) + strlen(args[1]) + 2 + strlen(args[2]) + 2 + strlen(args[3]) + 2 + strlen(args[4])];
            sprintf(buf, "%s%s, %s, %s, %s", str, args[1], args[2], args[3], args[4]);
            prof_win_show(plugin_win, buf);
        }
    } else if (strcmp(args[0], "constest") == 0) {
        int res = prof_current_win_is_console();
        create_win();
        prof_win_focus(plugin_win);
        if (res) {
            prof_win_show(plugin_win, "called -> prof_current_win_is_console: true");
        } else {
            prof_win_show(plugin_win, "called -> prof_current_win_is_console: false");
        }
    } else if (strcmp(args[0], "winshow") == 0) {
        if (args[1]) {
            create_win();
            prof_win_focus(plugin_win);
            prof_win_show(plugin_win, args[1]);
            char *str = "called -> prof_win_show: ";
            char buf[strlen(str) + strlen(args[1])];
            sprintf(buf, "%s%s", str, args[1]);
            prof_win_show(plugin_win, buf);
        } else {
            prof_cons_bad_cmd_usage("/c-test");
        }
    } else if (strcmp(args[0], "winshow_t") == 0) {
        if (args[1] == NULL || args[2] == NULL || args[3] == NULL || args[4] == NULL) {
            prof_cons_bad_cmd_usage("/c-test");
        } else {
            char *group = strcmp(args[1], "none") == 0 ? NULL : args[1];
            char *key = strcmp(args[2], "none") == 0 ? NULL : args[2];
            char *def = strcmp(args[3], "none") == 0 ? NULL : args[3];
            char *message = args[4];
            create_win();
            prof_win_focus(plugin_win);
            prof_win_show_themed(plugin_win, group, key, def, message);
            char *str = "called -> prof_win_show_themed: ";
            char buf[strlen(str) + strlen(args[1]) + 2 + strlen(args[2]) + 2 + strlen(args[3]) + 2 + strlen(args[4])];
            sprintf(buf, "%s%s, %s, %s, %s", str, args[1], args[2], args[3], args[4]);
            prof_win_show(plugin_win, buf);
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
    } else if (strcmp(args[0], "count") == 0) {
        create_win();
        prof_win_focus(plugin_win);
        char buf[100];
        sprintf(buf, "Count: %d", count);
        prof_win_show(plugin_win, buf);
    } else {
        prof_cons_bad_cmd_usage("/c-test");
    }
}

void
timed_callback(void)
{
    create_win();
    prof_win_show(plugin_win, "timed -> timed_callback called");
}

void
prof_init(const char * const version, const char * const status)
{
    pthread_create(&worker_thread, NULL, inc_counter, NULL);

    prof_win_create(plugin_win, handle_win_input);

    const char *synopsis[] = {
        "/c-test consalert",
        "/c-test consshow <message>",
        "/c-test consshow_t <group> <key> <default> <message>",
        "/c-test constest",
        "/c-test winshow <message>",
        "/c-test winshow_t <group> <key> <default> <message>",
        "/c-test notify <message>",
        "/c-test sendline <line>",
        "/c-test get recipient|room",
        "/c-test log debug|info|warning|error <message>",
        "/c-test count",
        NULL
    };
    const char *description = "C test plugin. All commands focus the plugin window.";
    const char *args[][2] = {
        { "consalert",                                      "Highlight the console window in the status bar" },
        { "consshow <message>",                             "Show the message in the console window" },
        { "consshow_t <group> <key> <default> <message>",   "Show the themed message in the console window. " },
        { "constest",                                       "Show whether the command was run in the console." },
        { "winshow <message>",                              "Show the message in the plugin window" },
        { "winshow_t <group> <key> <default> <message>",    "Show the themed message in the plugin window. " },
        { "notify <message>",                               "Send a desktop notification with message" },
        { "sendline <line>",                                "Pass line to profanity to process" },
        { "get recipient",                                  "Show the current chat recipient, if in a chat window" },
        { "get room",                                       "Show the current room JID, if in a chat room" },
        { "log debug|info|warning|error <message>",         "Log a message at the specified level" },
        { "count",                                          "Show the counter, incremented every 5 seconds by a worker thread" },
        { NULL, NULL }
    };

    const char *examples[] = {
        "/c-test sendline /about",
        "/c-test log debug \"Test debug message\"",
        "/c-test consshow_t c-test cons.show none \"This is themed\"",
        "/c-test consshow_t none none bold_cyan \"This is bold_cyan\"",
        NULL
    };

    prof_register_command("/c-test", 1, 5, synopsis, description, args, examples, cmd_ctest);

    char *cmd_ac[] = { "consalert", "consshow", "consshow_t", "constest", "winshow", "winshow_t", "notify", "sendline", "get", "log", "count", NULL };
    prof_register_ac("/c-test", cmd_ac);

    char *get_ac[] = { "recipient", "room", NULL };
    prof_register_ac("/c-test get", get_ac);

    char *log_ac[] = { "debug", "info", "warning", "error", NULL };
    prof_register_ac("/c-test log", log_ac);

    prof_register_timed(timed_callback, 30);
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
