/*
 * Copyright (C) 2020 Stefan Kropp <stefan@debxwoody.de>
 *
 * This file is part of profanity.
 *
 * profanity is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 3 of the License.
 *
 * profanity is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with profanity.  If not, see <http://www.gnu.org/licenses/>.
 *
 * File: c_plugin_example_01.c
 * 
 * Example 1 for profanity c plugin.
 *
 * This example implements the hooks (callbacks) provides by profanity. The
 * plugin writes name of function / the parameters of the hooks into a file.
 *
 * Compile: 
 *
 * gcc -shared -fpic -g3 -O0 -Wextra -pedantic \
 * -L/usr/lib/profanity -lprofanity \
 * -o c_plugin_example_01.so c_plugin_example_01.c
 *
 * Install:
 * 
 * cp c_plugin_example_01.so \
 * ~/.local/share/profanity/plugins/c_plugin_example_01.so
 *
 * Documentation:
 * 
 * https://profanity-im.github.io/plugins.html
 *
 */

#include <profapi.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

FILE *fp;

void prof_init(const char *const version, const char *const status,
               const char *const account_name, const char *const fulljid) {
  fp = fopen("profanity-c-plugins-example_01.log", "a");
  fprintf(fp, "prof_init: %s %s %s %s\n", version, status, account_name,
          fulljid);
  fflush(fp);
}

void prof_on_start(void) {
  fprintf(fp, "prof_on_start\n");
  fflush(fp);
}

void prof_on_shutdown(void) {
  fprintf(fp, "prof_on_shutdown\n");
  fflush(fp);
}

void prof_on_unload(void) {
  fprintf(fp, "prof_on_unload\n");
  fflush(fp);
  fclose(fp);
}

void prof_on_connect(const char *const account_name,
                     const char *const fulljid) {
  fprintf(fp, "prof_on_connect: %s %s\n", account_name, fulljid);
  fflush(fp);
}

void prof_on_disconnect(const char *const account_name,
                        const char *const fulljid) {
  fprintf(fp, "prof_on_disconnect: %s %s\n", account_name, fulljid);
  fflush(fp);
}

char *prof_pre_chat_message_display(const char *const barejid,
                                    const char *const resource,
                                    const char *message) {
  fprintf(fp, "prof_pre_chat_message_display: %s %s %s\n", barejid, resource,
          message);
  fflush(fp);
  return NULL;
}

void prof_post_chat_message_display(const char *const barejid,
                                    const char *const resource,
                                    const char *message) {
  fprintf(fp, "prof_post_chat_message_display %s %s %s\n", barejid, resource,
          message);
  fflush(fp);
}

char *prof_pre_chat_message_send(const char *const barejid,
                                 const char *message) {
  fprintf(fp, "prof_pre_chat_message_send: %s %s\n", barejid, message);
  fflush(fp);
  return strdup(message);
}

void prof_post_chat_message_send(const char *const barejid,
                                 const char *message) {
  fprintf(fp, "prof_post_chat_message_send: %s %s\n", barejid, message);
  fflush(fp);
}

char *prof_pre_room_message_display(const char *const barejid,
                                    const char *const nick,
                                    const char *message) {
  fprintf(fp, "prof_pre_room_message_display: %s %s %s\n", barejid, nick,
          message);
  fflush(fp);
  return NULL;
}

void prof_post_room_message_display(const char *const barejid,
                                    const char *const nick,
                                    const char *message) {
  fprintf(fp, "prof_post_room_message_display: %s %s %s\n", barejid, nick,
          message);
  fflush(fp);
}

char *prof_pre_room_message_send(const char *const barejid,
                                 const char *message) {
  fprintf(fp, "prof_pre_room_message_send %s %s\n", barejid, message);
  fflush(fp);
  return strdup(message);
}

void prof_post_room_message_send(const char *const barejid,
                                 const char *message) {
  fprintf(fp, "prof_post_room_message_send: %s %s\n", barejid, message);
  fflush(fp);
}

void prof_on_room_history_message(const char *const barejid,
                                  const char *const nick,
                                  const char *const message,
                                  const char *const timestamp) {
  fprintf(fp, "prof_on_room_history_message: %s %s %s %s\n", barejid, nick,
          message, timestamp);
  fflush(fp);
}

char *prof_pre_priv_message_display(const char *const barejid,
                                    const char *const nick,
                                    const char *message) {
  fprintf(fp, "prof_pre_priv_message_display: %s %s %s\n", barejid, nick,
          message);
  fflush(fp);
  return NULL;
}

void prof_post_priv_message_display(const char *const barejid,
                                    const char *const nick,
                                    const char *message) {
  fprintf(fp, "prof_post_priv_message_display: %s %s %s\n", barejid, nick,
          message);
  fflush(fp);
}

char *prof_pre_priv_message_send(const char *const barejid,
                                 const char *const nick, const char *message) {
  fprintf(fp, "prof_pre_priv_message_send: %s %s %s\n", barejid, nick, message);
  fflush(fp);
  return strdup(message);
}

void prof_post_priv_message_send(const char *const barejid,
                                 const char *const nick, const char *message) {
  fprintf(fp, "prof_post_priv_message_send: %s %s %s\n", barejid, nick,
          message);
  fflush(fp);
}

char *prof_on_message_stanza_send(const char *const stanza) {
  fprintf(fp, "prof_on_message_stanza_send: %d\n", strlen(stanza));
  fflush(fp);
  return NULL;
}

int prof_on_message_stanza_receive(const char *const stanza) {
  fprintf(fp, "prof_on_message_stanza_receive: %d\n", strlen(stanza));
  fflush(fp);
  return 1;
}

char *prof_on_presence_stanza_send(const char *const stanza) {
  fprintf(fp, "prof_on_presence_stanza_send: %s\n", stanza);
  fflush(fp);
  return NULL;
}

int prof_on_presence_stanza_receive(const char *const stanza) {
  fprintf(fp, "prof_on_presence_stanza_receive: %d\n", strlen(stanza));
  fflush(fp);
  return 1;
}

char *prof_on_iq_stanza_send(const char *const stanza) {
  fprintf(fp, "prof_on_iq_stanza_send: %d\n", strlen(stanza));
  fflush(fp);
  return NULL;
}

int prof_on_iq_stanza_receive(const char *const stanza) {
  fprintf(fp, "prof_on_iq_stanza_receive: %d\n", strlen(stanza));
  fflush(fp);
  return 1;
}

void prof_on_contact_offline(const char *const barejid,
                             const char *const resource,
                             const char *const status) {
  fprintf(fp, "prof_on_contact_offline: %s %s %s\n", barejid, resource, status);
  fflush(fp);
}

void prof_on_contact_presence(const char *const barejid,
                              const char *const resource,
                              const char *const presence,
                              const char *const status, const int priority) {
  fprintf(fp, "prof_on_contact_presence: %s %s %s %s %d\n", barejid, resource,
          presence, status, priority);
  fflush(fp);
}

void prof_on_chat_win_focus(const char *const barejid) {
  fprintf(fp, "prof_on_chat_win_focus: %s\n", barejid);
  fflush(fp);
}

void prof_on_room_win_focus(const char *const barejid) {
  fprintf(fp, "prof_on_room_win_focus: %s\n", barejid);
  fflush(fp);
}
