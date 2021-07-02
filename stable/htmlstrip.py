# -*- coding:utf-8 -*-
# vim: set ts=2 sw=2 sts=2 et:
"""
Author: Diego Blanco <diego.blanco@treitos.com>

Removes "unwanted" HTML tags from incoming messages and unescapes html.

Some XMPP clients like Adium or Pidgin send HTML tags like <font>, <b>, <u>, etc
to format text, specially when using OTR. This plugin removes them and also
unescapes HTML like &lt;, &gt;, etc that these clients also tend to escape.
"""

import re
import prof
import html

#( regular expressions
re_font   = re.compile('</?FONT(>| [^>]+>)', re.IGNORECASE)
re_br     = re.compile('</?BR>', re.IGNORECASE)
re_styles = re.compile('</?(U|B|I)>', re.IGNORECASE)
re_link   = re.compile('</?a(>| [^>]+>)', re.IGNORECASE)
#)

def _htmlstrip(message):
  """ Cleans message
  """
  try:
    _message = message
    _message = re_styles.sub( '', _message )
    _message = re_font.sub( '', _message )
    _message = re_br.sub( '\n', _message )
    _message = re_link.sub( '', _message )

    _message = html.unescape( _message )
  except:
    return ("ERR@htmlstrip.py: " + message)
  finally:
    return (_message)

def prof_pre_chat_message_display(barejid, resource, message):
    return _htmlstrip(message)

def prof_pre_room_message_display(barejid, nick, message):
    return _htmlstrip(message)

def prof_pre_priv_message_display(barejid, nick, message):
    return _htmlstrip(message)
