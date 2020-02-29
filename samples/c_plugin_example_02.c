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
 * File: c_plugin_example_02.c
 *
 * Example 2 for profanity c plugin. Define an own command which will be execute
 * your own function. Load the plugin and try /help example2.
 *
 * Compile:
 *
 * gcc -shared -fpic -g3 -O0 -Wextra -pedantic \
 * -L/usr/lib/profanity -lprofanity \
 * -o c_plugin_example_02.so c_plugin_example_02.c
 *
 * Install:
 *
 * cp c_plugin_example_02.so \
 * ~/.local/share/profanity/plugins/
 *
 * Documentation:
 *
 * https://profanity-im.github.io/plugins.html
 *
 */
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

#include <profapi.h>

void cmd_callback(char **args) {
  prof_cons_show("Hello! I'm Example 2.");
  prof_cons_alert();
}

void prof_init(const char *const version, const char *const status,
               const char *const account_name, const char *const fulljid) {
  char *synopsis[] = {"/example2", NULL};
  char *description = "Example 2 for profanity c plugin.";
  char *args[][2] = {{NULL, NULL}};
  char *examples[] = {NULL};

  prof_register_command(synopsis[0], 0, 0, synopsis, description, args,
                        examples, cmd_callback);
}
