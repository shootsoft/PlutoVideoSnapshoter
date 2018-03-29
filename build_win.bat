pyinstaller -F -w --icon=res/pluto.ico ^
          --add-data "src\windows;windows" ^
          --add-data "venv/v36/Lib/site-packages/cv2/opencv_ffmpeg340.dll;./"  ^
          --path "C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x86" ^
          --version-file=file_version_info.txt "src\app.py" ^
          -n "PlutoVideoSnapshoter"

goto comment
...skip this...
REM Multiple files, for debugging
pyinstaller -D -w --icon=res/pluto.ico ^
          --add-data "src\windows;windows" ^
          --add-data "venv/v36/Lib/site-packages/cv2/opencv_ffmpeg340.dll;./"  ^
          --path "C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x86" ^
          --version-file=file_version_info.txt "src\app.py" ^
          -n "PlutoVideoSnapshoter"

:comment
