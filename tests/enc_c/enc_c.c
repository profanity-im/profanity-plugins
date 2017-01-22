#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

#include <profapi.h>

static char *chat_msg_hook = NULL;
static char *room_msg_hook = NULL;

void
cmd_enc(char **args)
{
    if (args[0] && strcmp(args[0], "end") == 0) {
        prof_encryption_reset(args[1]);

    } else if (args[0] && (strcmp(args[0], "chat_title") == 0)) {
        if (args[1] && (strcmp(args[1], "set") == 0)) {
            prof_chat_set_titlebar_enctext(args[2], args[3]);
        } else if (args[1] && (strcmp(args[1], "reset") == 0)) {
            prof_chat_unset_titlebar_enctext(args[2]);
        } else {
            prof_cons_bad_cmd_usage("/enc_c");
        }

    } else if (args[0] && (strcmp(args[0], "chat_ch") == 0)) {
        if (args[1] && (strcmp(args[1], "set") == 0)) {
            if (args[2] && (strcmp(args[2], "in") == 0)) {
                prof_chat_set_incoming_char(args[3], args[4]);
            } else if (args[2] && (strcmp(args[2], "out") == 0)) {
                prof_chat_set_outgoing_char(args[3], args[4]);
            } else {
                prof_cons_bad_cmd_usage("/enc_c");
            }
        } else if (args[1] && (strcmp(args[1], "reset") == 0)) {
            if (args[2] && (strcmp(args[2], "in") == 0)) {
                prof_chat_unset_incoming_char(args[3]);
            } else if (args[2] && (strcmp(args[2], "out") == 0)) {
                prof_chat_unset_outgoing_char(args[3]);
            } else {
                prof_cons_bad_cmd_usage("/enc_c");
            }
        } else {
            prof_cons_bad_cmd_usage("/enc_c");
        }

    } else if (args[0] && (strcmp(args[0], "room_title") == 0)) {
        if (args[1] && (strcmp(args[1], "set") == 0)) {
            prof_room_set_titlebar_enctext(args[2], args[3]);
        } else if (args[1] && (strcmp(args[1], "reset") == 0)) {
            prof_room_unset_titlebar_enctext(args[2]);
        } else {
            prof_cons_bad_cmd_usage("/enc_c");
        }

    } else if (args[0] && (strcmp(args[0], "room_ch") == 0)) {
        if (args[1] && (strcmp(args[1], "set") == 0)) {
            prof_room_set_message_char(args[2], args[3]);
        } else if (args[1] && (strcmp(args[1], "reset") == 0)) {
            prof_room_unset_message_char(args[2]);
        } else {
            prof_cons_bad_cmd_usage("/enc_c");
        }

    } else if (args[0] && (strcmp(args[0], "chat_show") == 0)) {
        prof_chat_show(args[1], args[2]);
    
    } else if (args[0] && (strcmp(args[0], "chat_show_themed") == 0)) {
        prof_chat_show_themed(args[1], "enc_c", "chat_msg", NULL, "c", args[2]);

    } else if (args[0] && (strcmp(args[0], "room_show") == 0)) {
        prof_room_show(args[1], args[2]);
    
    } else if (args[0] && (strcmp(args[0], "room_show_themed") == 0)) {
        prof_room_show_themed(args[1], "enc_c", "room_msg", NULL, "C", args[2]);

    } else if (args[0] && (strcmp(args[0], "chat_msg") == 0)) {
        if (chat_msg_hook) {
            free(chat_msg_hook);
        }
        chat_msg_hook = strdup(args[1]);

    } else if (args[0] && (strcmp(args[0], "room_msg") == 0)) {
        if (room_msg_hook) {
            free(room_msg_hook);
        }
        room_msg_hook = strdup(args[1]);

    } else {
        prof_cons_bad_cmd_usage("/enc_c");
    }
}

void
prof_init(const char * const version, const char * const status, const char *const account_name, const char *const fulljid)
{
    char *synopsis[] = { 
        "/enc_c end <barejid>",
        "/enc_c chat_title set <barejid> <text>",
        "/enc_c chat_title unset <barejid>",
        "/enc_c chat_ch set in <barejid> <ch>",
        "/enc_c chat_ch reset in <barejid>",
        "/enc_c chat_ch set out <barejid> <ch>",
        "/enc_c chat_ch reset out <barejid>",
        "/enc_c chat_show <barejid> <message>",
        "/enc_c chat_show_themed <barejid> <message>",
        "/enc_c room_title set <roomjid> <text>",
        "/enc_c room_title unset <roomjid>",
        "/enc_c room_ch set <roomjid> <ch>",
        "/enc_c room_ch reset <roomjid>",
        "/enc_c room_show <roomjid> <message>",
        "/enc_c room_show_themed <roomjid> <message>",
        "/enc_c chat_msg none",
        "/enc_c chat_msg modify",
        "/enc_c chat_msg block",
        "/enc_c room_msg none",
        "/enc_c room_msg modify",
        "/enc_c room_msg block",
        NULL
    };
    char *description = "Various enc things";
    char *args[][2] = { 
        { "end <barejid>",                          "User to end the session with" },
        { "chat_title set <barejid> <text>",        "Set encryption text in titlebar for recipient" },
        { "chat_title reset <barejid>",             "Reset encryption text in titlebar for recipient" },
        { "chat_ch set in <barejid> <ch>",          "Set incoming char for recipient" },
        { "chat_ch reset in <barejid>",             "Reset incoming char for recipient" },
        { "chat_ch set out <barejid> <ch>",         "Set outgoing char for recipient" },
        { "chat_ch reset out <barejid>",            "Reset outgoing char for recipient" },
        { "chat_show <barejid> <message>",          "Show chat message" },
        { "chat_show_themed <barejid> <message>",   "Show themed chat message" },
        { "room_title set <roomjid> <text>",        "Set encryption text in titlebar for room" },
        { "room_title reset <roomjid>",             "Reset encryption text in titlebar for room" },
        { "room_ch set <roomjid> <ch>",             "Set char for room" },
        { "room_ch reset <roomjid>",                "Reset char for room" },
        { "room_show <roomjid> <message>",          "Show chat room message" },
        { "room_show_themed <roomjid> <message>",   "Show themed chat room message" },
        { "chat_msg none",                          "Preserve chat messages" },
        { "chat_msg modify",                        "Modify chat messages" },
        { "chat_msg block",                         "Block chat messages" },
        { "room_msg none",                          "Preserve chat room messages" },
        { "room_msg modify",                        "Modify chat room messages" },
        { "room_msg block",                         "Block chat room messages" },
        { NULL, NULL } 
    };
    char *examples[] = { NULL };

    prof_register_command("/enc_c", 2, 5, synopsis, description, args, examples, cmd_enc);
 
    char *cmd_ac[] = {
        "end",
        "chat_title",
        "chat_ch",
        "chat_show",
        "chat_show_themed",
        "room_title",
        "room_ch",
        "room_show",
        "room_show_themed",
        "chat_msg",
        "room_msg",
        NULL
    };
    prof_completer_add("/enc_c", cmd_ac);

    char *chat_title_ac[] = { "set", "reset", NULL };
    prof_completer_add("/enc_c chat_title", chat_title_ac);

    char *chat_ch_ac[] = { "set", "reset", NULL };
    prof_completer_add("/enc_c chat_ch", chat_ch_ac);

    char *chat_ch_set_ac[] = { "in", "out", NULL };
    prof_completer_add("/enc_c chat_ch set", chat_ch_set_ac);

    char *chat_ch_reset_ac[] = { "in", "out", NULL };
    prof_completer_add("/enc_c chat_ch reset", chat_ch_reset_ac);

    char *room_title_ac[] = { "set", "reset", NULL };
    prof_completer_add("/enc_c room_title", room_title_ac);

    char *room_ch_ac[] = { "set", "reset", NULL };
    prof_completer_add("/enc_c room_ch", room_ch_ac);

    char *chat_msg_ac[] = { "none", "modify", "block", NULL };
    prof_completer_add("/enc_c chat_msg", chat_msg_ac);

    char *room_msg_ac[] = { "none", "modify", "block", NULL };
    prof_completer_add("/enc_c room_msg", room_msg_ac);
}

char*
prof_pre_chat_message_send(const char * const barejid, const char *message)
{
    if (chat_msg_hook && (strcmp(chat_msg_hook, "modify") == 0)) {
        char buf[strlen("[c modified] ") + strlen(message) + 1];
        sprintf(buf, "%s%s", "[c modified] ", message);
        return strdup(buf);
    } else if (chat_msg_hook && (strcmp(chat_msg_hook, "block") == 0)) {
        prof_chat_show_themed(barejid, NULL, NULL, "bold_red", "!", "C plugin blocked message");
        return NULL;
    } else {
        return strdup(message);
    }
}

char*
prof_pre_room_message_send(const char * const roomjid, const char *message)
{
    if (room_msg_hook && (strcmp(room_msg_hook, "modify") == 0)) {
        char buf[strlen("[c modified] ") + strlen(message) + 1];
        sprintf(buf, "%s%s", "[c modified] ", message);
        return strdup(buf);
    } else if (room_msg_hook && (strcmp(room_msg_hook, "block") == 0)) {
        prof_room_show_themed(roomjid, NULL, NULL, "bold_red", "!", "C plugin blocked message");
        return NULL;
    } else {
        return strdup(message);
    }
}