@echo off
REM ============================================
REM Convert Mishnah Articles to TXT for NotebookLM
REM ============================================
REM Place this file in the Articles folder and run it
REM Source: C:\My Web Sites\Site Download May 14 2025\Mishnah-New\English\Articles
REM ============================================

setlocal enabledelayedexpansion

REM Create output folder for txt files
set "OUTPUT_DIR=NotebookLM_Upload"
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo.
echo Converting article files to .txt format...
echo Output folder: %OUTPUT_DIR%
echo.

set count=0

REM Process HTML files
for %%f in (*.html *.htm) do (
    copy "%%f" "%OUTPUT_DIR%\%%~nf.txt" >nul 2>&1
    if !errorlevel! equ 0 (
        echo Converted: %%f
        set /a count+=1
    )
)

REM Process any existing text-based files that aren't .txt
for %%f in (*.md *.xml) do (
    copy "%%f" "%OUTPUT_DIR%\%%~nf.txt" >nul 2>&1
    if !errorlevel! equ 0 (
        echo Converted: %%f
        set /a count+=1
    )
)

echo.
echo ============================================
echo Conversion complete!
echo Total files converted: %count%
echo Files saved to: %CD%\%OUTPUT_DIR%
echo ============================================
echo.
pause
