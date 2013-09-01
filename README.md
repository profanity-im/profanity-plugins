profanity-plugins
=================

Plugin support for Profanity is currently in development at the `plugins` branch.

Building Profanity with plugin support
--------------------------------------

Check out the `plugins` branch and run the usual:

```
./bootstrap.sh
./configure
make
sudo make install
```

The last step will create a shared library `libprofanity` and install headers required for developing C plugins.  If you don't want to run any C plugins, you can omit the last step.

You will need python-dev, ruby-dev and libtool packages installed on your system.

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

Example plugin code
-------------------

Whilst the API is being developed, the following test plugins are a good reference of possible hooks and API calls available:

```
python-test.py
RubyTest.rb
test-c-plugin/*
```

