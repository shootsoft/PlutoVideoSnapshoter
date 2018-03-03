pyinstaller -F -w --icon=res/pluto.ico --add-data "src\windows;windows" --path "C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x86" "src\app.py"
