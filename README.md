profanity-plugins
=================

Plugin support for Profanity is currently in development at the `plugins` branch.

Supported languages for writing plugins are C, Python, Ruby and Lua.

![alt tag](http://www.profanity.im/cricket.png)

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

A wrapper script is included to enable support for stable plugin languages:

```
./configure-plugins
```

This script forces support for C, Python and Ruby.  Lua support for all platforms is still in progress.

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
load=browser.py;connect.lua;ChatStart.rb;cricket-score.py;platform-info.py;ascii.py;pid.so
```

Run the `/plugins` command to see a list of installed plugins.

Example plugin code
-------------------

Whilst the API is being developed, the following test plugins are a good reference of possible hooks and API calls available:

```
python-test.py
RubyTest.rb
luatest.lua
test-c-plugin/test-c-plugin.c
```
