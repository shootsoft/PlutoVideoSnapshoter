#!/bin/sh

echo "Creating app file..."
rm -rf dist
pyinstaller -D -w mac_build.spec
echo "app created."

if [ "$1" == "dmg" ]; then

    if [ -n "$2" ]; then
        echo "Signing..."
        codesign -s "$2" dist/PlutoVideoSnapshoter.app --deep
        echo "Verify signing..."
        codesign -dv --verbose=4 dist/PlutoVideoSnapshoter.app
    fi

    echo "Creating dmg file..."
    dmgbuild -s dmg_settings.py "PlutoVideoSnapshoter Volume" PlutoVideoSnapshoter.dmg

    if [ -n "$2" ]; then
        echo "Signing..."
        codesign -s "$2" PlutoVideoSnapshoter.dmg
        echo "Verify signing..."
        codesign -dv --verbose=4 PlutoVideoSnapshoter.dmg
        echo "DMG created."
    fi
fi

echo "All done."
# Multiple files, for debugging

#pyinstaller --clean -F -w \
#        --icon=res/pluto.icns \
#        --add-data "src/windows:windows"  \
#        "src/app.py" \
#        -n "PlutoVideoSnapshoter"

