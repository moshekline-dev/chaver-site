@echo off
REM Collect all Genesis unit and commentary files for NotebookLM upload
REM Run this from your site root folder (e.g., C:\My Web Sites\Site Download May 14 2025)

REM Create output folder
mkdir "NotebookLM-Genesis" 2>nul

REM Copy unit text files and commentaries from each unit folder
for /D %%d in (Genesis\genesis-unit-*) do (
    for %%f in ("%%d\*.html") do (
        echo Copying %%f
        copy "%%f" "NotebookLM-Genesis\%%~nf.txt"
    )
)

REM Also copy the overview/structural files from genesis-analysis and genesis-matrix-slides
if exist "Genesis\genesis-analysis\units-of-genesis.html" (
    copy "Genesis\genesis-analysis\units-of-genesis.html" "NotebookLM-Genesis\units-of-genesis.txt"
)
if exist "Genesis\genesis-analysis\the-map-of-genesis.html" (
    copy "Genesis\genesis-analysis\the-map-of-genesis.html" "NotebookLM-Genesis\the-map-of-genesis.txt"
)
if exist "Genesis\genesis-analysis\the-three-rows.html" (
    copy "Genesis\genesis-analysis\the-three-rows.html" "NotebookLM-Genesis\the-three-rows.txt"
)
if exist "Genesis\genesis-analysis\architecture-and-meaning-in-genesis.html" (
    copy "Genesis\genesis-analysis\architecture-and-meaning-in-genesis.html" "NotebookLM-Genesis\architecture-and-meaning-in-genesis.txt"
)
if exist "Genesis\genesis-analysis\overview.html" (
    copy "Genesis\genesis-analysis\overview.html" "NotebookLM-Genesis\overview.txt"
)

echo.
echo === DONE ===
echo Files collected in NotebookLM-Genesis folder
echo.
dir "NotebookLM-Genesis\*.txt"
pause
