#!/bin/sh

rm -rf dist
pyinstaller -D -w mac_build.spec

# Multiple files, for debugging

#pyinstaller --clean -F -w \
#        --icon=res/pluto.icns \
#        --add-data "src/windows:windows"  \
#        "src/app.py" \
#        -n "PlutoVideoSnapshoter"

