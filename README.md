profanity-plugins
=================

Plugin support for Profanity is currently in development at the `plugins` branch.

Supported languages for writing plugins are C, Python, Ruby and Lua.

Building Profanity with plugin support
--------------------------------------

`autoconf-archive`, `libtool` and the development packages for each supported langauge are required e.g.:

```
python-dev
lua-dev
ruby-dev
```

Check out the `plugins` branch and run the usual:

```
./bootstrap.sh
./configure
make
sudo make install
```

By default, support for each language is optional and will be attempted during `./configure`.  To force support for a language, or disable support, the following flags may be used with `./configure`.

```
--enable-c-plugins, --disable-c-plugins
--enable-python-plugins, --disable-python-plugins
--enable-ruby-plugins, --disable-ruby-plugins
--enable-lua-plugins, --disable-lua-plugins
```

A wrapper script is included to enable support for currently stable plugin languages:

```
./configure-plugins
```

This script currently forces support for C and Python.  Ruby and Lua support for all platforms is still in progress.

Loading plugins
---------------

1. Copy the plugin

For Python, Ruby and Lua plugins, copy the plugin to `$XDG_DATA/profanity/plugins/`, (`~/.local/share/profanity/plugins/` on most systems).

For C plugins, build the plugin using the supplied Makefile, and then copy the `.so` file to the same location.

2. Add to profrc

For all types of plugins, the list of plugins to acutally load when starting Profanity is defined in `$XDG_CONFIG/profanity/profrc` (`~/.config/profanity/profrc` on most systems).

For example:

```
[plugins]
load=browser.py;connect.lua;ChatStart.rb;platform-info.py;ascii.py;pid.so
```

Run the `/plugins` command to see a list of installed plugins.

Example plugin code
-------------------

Whilst the API is being developed, the following test plugins are a good reference of possible hooks and API calls available:

```
tests/python-test.py
tests/RubyTest.rb
tests/luatest.lua
tests/test-c-plugin/test-c-plugin.c
```

Jenkins plugin
--------------

The jenkins plugin monitors builds at a jenkins server and notifies of build status changes, builds may be triggered, logs viewed, and jobs opened using the system's default browser.

![alt tag](http://www.boothj5.com/jenkins-plugin.png)
