# Ch07 Enhanced SDD Generation Script (PowerShell)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Ch07 Enhanced SDD Generation Script v2.0" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Generate Diagrams
Write-Host "[Step 1/3] Generating all diagrams (including UI wireframes)..." -ForegroundColor Yellow
python create_diagrams.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Diagram generation failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Diagrams generated successfully" -ForegroundColor Green
Write-Host ""

# Step 2: Generate Enhanced PDF
Write-Host "[Step 2/3] Generating Enhanced SDD PDF v2.0..." -ForegroundColor Yellow
python create_master_sdd.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: PDF generation failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ PDF generated successfully" -ForegroundColor Green
Write-Host ""

# Step 3: Git Commit
Write-Host "[Step 3/3] Committing changes to Git..." -ForegroundColor Yellow
git add create_diagrams.py create_master_sdd.py Ch07_SDD_Enhanced.pdf diagrams/*.png generate_enhanced_sdd.ps1 generate_enhanced_sdd.bat ENHANCEMENT_SUMMARY.md
git commit -m "Add Enhanced SDD v2.0 with UI wireframes and improved content

- Added 4 UI mockups (dashboard, heatmap, timeline, feature importance)
- Enhanced formatting with professional blue theme
- Expanded content with executive summary and detailed tables
- Improved diagram captions and figure numbering
- Added comprehensive appendices with feature dictionary"

if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Git commit failed (may be nothing to commit)" -ForegroundColor Yellow
} else {
    Write-Host "✓ Changes committed to Git" -ForegroundColor Green
    
    # Try to push
    git push
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Changes pushed to remote repository" -ForegroundColor Green
    } else {
        Write-Host "WARNING: Git push failed" -ForegroundColor Yellow
    }
}
Write-Host ""

# Summary
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SUCCESS! Enhanced SDD generation complete." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Output file: Ch07_SDD_Enhanced.pdf" -ForegroundColor White
Write-Host ""

# Check file size
if (Test-Path "Ch07_SDD_Enhanced.pdf") {
    $fileSize = (Get-Item "Ch07_SDD_Enhanced.pdf").Length
    $fileSizeKB = [math]::Round($fileSize / 1KB, 2)
    $fileSizeMB = [math]::Round($fileSize / 1MB, 2)
    Write-Host "File size: $fileSizeKB KB ($fileSizeMB MB)" -ForegroundColor Cyan
}

# List generated diagrams
Write-Host ""
Write-Host "Generated diagrams:" -ForegroundColor Yellow
if (Test-Path "diagrams") {
    Get-ChildItem "diagrams\*.png" | ForEach-Object {
        Write-Host "  - $($_.Name)" -ForegroundColor Gray
    }
}

Write-Host ""
Read-Host "Press Enter to exit"
