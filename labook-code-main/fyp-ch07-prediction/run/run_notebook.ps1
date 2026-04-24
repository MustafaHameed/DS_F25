$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$notebookPath = Resolve-Path (Join-Path $projectRoot "..\ch07-prediction\ch07-prediction.ipynb")

Set-Location (Split-Path $notebookPath.Path)

if (Get-Command jupyter -ErrorAction SilentlyContinue) {
    jupyter lab $notebookPath.Path
} else {
    throw "Jupyter was not found on PATH. Install Jupyter Lab or Notebook before launching the Chapter 07 notebook."
}