@echo off
echo ============================================================
echo Ch07 Enhanced SDD Generation Script
echo ============================================================
echo.

echo [Step 1/3] Generating all diagrams (including UI wireframes)...
python create_diagrams.py
if %errorlevel% neq 0 (
    echo ERROR: Diagram generation failed!
    pause
    exit /b 1
)
echo.

echo [Step 2/3] Generating Enhanced SDD PDF v2.0...
python create_master_sdd.py
if %errorlevel% neq 0 (
    echo ERROR: PDF generation failed!
    pause
    exit /b 1
)
echo.

echo [Step 3/3] Committing changes to Git...
git add create_diagrams.py create_master_sdd.py Ch07_SDD_Enhanced.pdf diagrams/*.png
git commit -m "Add Enhanced SDD v2.0 with UI wireframes and improved content"
git push
if %errorlevel% neq 0 (
    echo WARNING: Git push failed or nothing to commit
)
echo.

echo ============================================================
echo SUCCESS! Enhanced SDD generation complete.
echo ============================================================
echo Output file: Ch07_SDD_Enhanced.pdf
echo.
pause
