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
 * !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 * !!!    Status: Development, not ready to use !!!!
 * !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 *
 * File: microblog.c
 *
 * The microblog plugin can be used for Movim Users. If profanity gets a message
 * "urn:xmpp:microblog:0", it will display the from, title and ID information of
 * the blog post.
 *
 * Profanity will display a message like this, in the main Window:
 *
 * Blog from user@domain.tld - Title of the post (ID of the post)
 *
 *
 * Compile:
 *
 * gcc -shared -fpic -g3 -O0 -Wextra -pedantic \
 * -L/usr/lib/profanity -lprofanity `pkg-config --libs --cflags libxml-2.0` \
 * -o microblog.so microblog.c
 *
 * Install:
 *
 * cp microblog.so \
 * ~/.local/share/profanity/plugins/
 *
 * Documentation:
 *
 * https://profanity-im.github.io/plugins.html
 *
 */

#include <profapi.h>

#include <libxml/parser.h>
#include <libxml/xpath.h>
#include <libxml/xpathInternals.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#define XMPP_URN_MICROBLOG "urn:xmpp:microblog:0"

typedef struct {
  char *id;
  char *from;
  char *title;
} PubSubEvent;

static bool enabled = true;

bool parse(const char *stanza, PubSubEvent *event) {
  xmlDocPtr doc;
  xmlNode *root_element = NULL;

  doc = xmlReadMemory(stanza, strlen(stanza), NULL, NULL, 0);
  if (doc == NULL) {
    return false;
  }

  xmlXPathContextPtr xpathCtx = xmlXPathNewContext(doc);
  xmlXPathRegisterNs(xpathCtx, BAD_CAST "ev",
                     BAD_CAST "http://jabber.org/protocol/pubsub#event");
  xmlXPathRegisterNs(xpathCtx, BAD_CAST "a",
                     BAD_CAST "http://www.w3.org/2005/Atom");

  xmlXPathObjectPtr xpathObj = xmlXPathEvalExpression(
      "//message/ev:event/ev:items/attribute::node", xpathCtx);
  if (strcmp(xpathObj->nodesetval->nodeTab[0]->children->content,
             XMPP_URN_MICROBLOG) == 0) {

    xpathObj = xmlXPathEvalExpression("//message/attribute::from", xpathCtx);
    event->from = strdup(xpathObj->nodesetval->nodeTab[0]->children->content);
    xmlXPathFreeObject(xpathObj);

    xpathObj = xmlXPathEvalExpression(
        "//message/ev:event/ev:items/ev:item/a:entry/a:title", xpathCtx);
    event->title = strdup(xpathObj->nodesetval->nodeTab[0]->children->content);
    xmlXPathFreeObject(xpathObj);

    xpathObj = xmlXPathEvalExpression(
        "//message/ev:event/ev:items/ev:item/attribute::id", xpathCtx);
    event->id = strdup(xpathObj->nodesetval->nodeTab[0]->children->content);
    xmlXPathFreeObject(xpathObj);
  } else {
    return false;
  }

  xmlXPathFreeContext(xpathCtx);
  xmlFreeDoc(doc);
  return true;
}

void prof_init(const char *const version, const char *const status,
               const char *const account_name, const char *const fulljid) {}

void prof_on_start(void) {}

void prof_on_shutdown(void) {}

void prof_on_unload(void) {}

int prof_on_message_stanza_receive(const char *const stanza) {
  if (enabled) {

    PubSubEvent event;
    event.id = NULL;
    event.from = NULL;
    event.title = NULL;
    if (parse(stanza, &event)) {
      int size =
          strlen(event.id) + strlen(event.from) + strlen(event.title) + 30;
      char *message = calloc(size, sizeof(char));
      snprintf(message, size, "Blog from %s - %s (%s)", event.from, event.title,
               event.id);
      prof_cons_show(message);
      prof_cons_alert();
    }
  }
  return 1;
}
