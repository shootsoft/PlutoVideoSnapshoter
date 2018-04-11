#!/bin/sh

rm -rf dist
pyinstaller -D -w mac_build.spec

if [ "$1" == "dmg" ]; then
    echo "Creating dmg file..."
    dmgbuild -s dmg_settings.py "PlutoVideoSnapshoter Volume" PlutoVideoSnapshoter.dmg
    echo "DMG created."
fi

echo "All done."
# Multiple files, for debugging

#pyinstaller --clean -F -w \
#        --icon=res/pluto.icns \
#        --add-data "src/windows:windows"  \
#        "src/app.py" \
#        -n "PlutoVideoSnapshoter"

