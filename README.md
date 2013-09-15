profanity-plugins
=================

Plugin support for Profanity is currently in development at the `plugins` branch.

Currently supported languages for writing plugins are C, Python, Ruby and Lua.

Building Profanity with plugin support
--------------------------------------

You will need a few more dependencies installed on your system:

```
python-dev
lua-dev
ruby-dev
libtool
autoconf-archive
```

Check out the `plugins` branch and run the usual:

```
./bootstrap.sh
./configure
make
sudo make install
```

The last step will create a shared library `libprofanity` and install headers required for developing C plugins.

Loading plugins
---------------

1. Copy the plugin

For Python and Ruby plugins, copy the plugin to `$XDG_DATA/profanity/plugins/`, (`~/.local/share/profanity/plugins/` on most systems).

For C plugins, build the plugin using the supplied Makefile, and then copy the `.so` file to the same location.

2. Add to profrc

For all types of plugins, the list of plugins to acutally load when starting Profanity is defined in `$XDG_CONFIG/profanity/profrc` (`~/.config/profanity/profrc` on most systems).

For example:

```
[plugins]
load=browser.py;connect.py;ChatStart.rb;cricket-score.py;platform-info.py;whoami.py;ascii.py                   
```

Run the `/plugins` command to see a list of installed plugins.

Example plugin code
-------------------

Whilst the API is being developed, the following test plugins are a good reference of possible hooks and API calls available:

```
python-test.py
RubyTest.rb
luatest.lua
test-c-plugin/*
```

