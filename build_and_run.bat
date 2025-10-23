@echo off
setlocal enabledelayedexpansion

echo Starting LaTeX compilation process...

REM Function to check if a command exists
where xelatex >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: xelatex not found in PATH. Please check your LaTeX installation.
    pause
    exit /b 1
)

where biber >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: biber not found in PATH. Please check your LaTeX installation.
    pause
    exit /b 1
)

REM Clean auxiliary files
echo Cleaning auxiliary files...
del /Q *.aux *.toc *.log *.out *.bbl *.bcf *.blg *.run.xml *.fdb_latexmk *.fls *.synctex.gz 2>nul

REM Compilation passes
for /L %%i in (1,1,3) do (
    echo Compilation pass %%i...
    xelatex -interaction=nonstopmode -file-line-error main.tex > compile.log 2>&1
    if !ERRORLEVEL! neq 0 (
        echo Error in compilation pass %%i! Check compile.log for details.
        type compile.log
        pause
        exit /b !ERRORLEVEL!
    )
    
    REM Run biber after first pass
    if %%i equ 1 (
        echo Processing bibliography...
        biber main > biber.log 2>&1
        if !ERRORLEVEL! neq 0 (
            echo Error in bibliography processing! Check biber.log for details.
            type biber.log
            pause
            exit /b !ERRORLEVEL!
        )
    )
)

echo Compilation successful! Opening PDF...
if exist main.pdf (
    start main.pdf
) else (
    echo Warning: PDF file not found!
)

pause