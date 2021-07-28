@echo off
setlocal enabledelayedexpansion

REM last Index, but not num of python.exe's path
set LAST_INDEX=1
set ARRAY[0]="%ProgramFiles%\Orange\python.exe"
set ARRAY[1]="%ProgramFiles%\Orange\Scripts\python.exe"

for /l %%n in (0,1,!LAST_INDEX!) do (
  rem echo "PATH:"!ARRAY[%%n]!
  if exist !ARRAY[%%n]! (
     echo "[OK] FOUND Python.exe: "!ARRAY[%%n]!
     !ARRAY[%%n]! -m pip install -U -e git+https://github.com/HirotsuguMINOWA/OC-NLP@master#egg=nlp4oc
     goto :COMPLETE
  ) else (
     echo "[NG] NOT FOUND Python.exe: "!ARRAY[%%n]!
  )
)
echo "FAILED. If orange canvas was installed into the custom path, Please consult with MINOWA."
pause
exit /b

:COMPLETE
  echo "Succeeded to install NLP4OC add-on."
  pause
  exit /b