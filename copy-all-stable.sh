rm -rf ~/.local/share/profanity/plugins/*

cp ascii.py ~/.local/share/profanity/plugins/.
cp syscmd.py ~/.local/share/profanity/plugins/.
cp paste.py ~/.local/share/profanity/plugins/.
cp browser.py ~/.local/share/profanity/plugins/.
cp platform-info.py ~/.local/share/profanity/plugins/.
cp say.py ~/.local/share/profanity/plugins/.
cp whoami.py ~/.local/share/profanity/plugins/.
cp wikipedia-prof.py ~/.local/share/profanity/plugins/.
cp tests/python-test.py ~/.local/share/profanity/plugins/.

cd pid
make clean
make
cp pid.so ~/.local/share/profanity/plugins/.
cd ..

cd tests/test-c-plugin
make clean
make
cp test-c-plugin.so ~/.local/share/profanity/plugins/.
cd ../..


