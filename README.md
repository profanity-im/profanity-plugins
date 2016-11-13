profanity-plugins
=================

* [Website documentation](http://www.profanity.im/plugins.html)

Building Profanity with plugin support
--------------------------------------

Dependencies required:

```
autoconf-archive
libtool
```

For Python plugins the following is also required:

```
python-dev
```

Installing plugins
------------------

Use the `/plugins install` command, e.g.

```
/plugins install ~/projects-git/profanity-plugins/stable/say.py
```

See the `/help plugins` command for further plugin management options.

Branches
--------

* `0.5.0`: Maintenance branch for plugins compatible with the current Profanity release 0.5.0
* `0.5.1`: Development for the next Profanity patch release 0.5.1
* `master`: Development for the next Profanity major release 0.6.0

Developing plugins
------------------

API Documentation:
* [Python API](http://www.profanity.im/plugins/python/html/prof.html)
* [Python hooks](http://www.profanity.im/plugins/python/html/plugin.html)
* [C API](http://www.profanity.im/plugins/c/html/profapi_8h.html)
* [C hooks](http://www.profanity.im/plugins/c/html/profhooks_8h.html)

