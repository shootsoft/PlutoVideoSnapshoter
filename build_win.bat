pyinstaller -F -w --icon=res/pluto.ico ^
          --add-data "src\windows;windows" ^
          --add-data "venv/v36/Lib/site-packages/cv2/opencv_ffmpeg330.dll;./"  ^
          --path "C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x86" ^
          --version-file=file_version_info.txt "src\app.py" ^
          -n "PlutoVideoSnapshoter"

IF [%1] == [] GOTO end
"C:\Program Files (x86)\Windows Kits\10\bin\x86\signtool.exe" sign ^
           /f Certificates.pfx /p %1 /t "http://timestamp.comodoca.com" ^
           "dist\PlutoVideoSnapshoter.exe"
GOTO end
...skip this...
REM Multiple files, for debugging
pyinstaller -D -w --icon=res/pluto.ico ^
          --add-data "src\windows;windows" ^
          --add-data "venv/v36/Lib/site-packages/cv2/opencv_ffmpeg330.dll;./"  ^
          --path "C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x86" ^
          --version-file=file_version_info.txt "src\app.py" ^
          -n "PlutoVideoSnapshoter"

:end
