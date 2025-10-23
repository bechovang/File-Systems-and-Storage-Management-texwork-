@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%" >nul

rem Detect Python
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  set "PY=python"
) else (
  where py >nul 2>nul
  if %ERRORLEVEL% EQU 0 (
    set "PY=py -3"
  ) else (
    echo Python not found. Please install Python 3 and ensure it is on PATH.
    popd >nul
    exit /b 1
  )
)

if "%~1"=="" (
  echo Running default: main.tex + bibliography.bib
  %PY% "%SCRIPT_DIR%tex_metrics.py" --tex "%SCRIPT_DIR%main.tex" --bib "%SCRIPT_DIR%bibliography.bib" --output text
) else (
  %PY% "%SCRIPT_DIR%tex_metrics.py" %*
)

set ERR=%ERRORLEVEL%
popd >nul
exit /b %ERR%


pause