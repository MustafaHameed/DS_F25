$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$notebookPath = Resolve-Path (Join-Path $projectRoot "..\ch13-multichannel\ch13-multichannel.ipynb")

Set-Location (Split-Path $notebookPath.Path)

if (Get-Command jupyter -ErrorAction SilentlyContinue) {
    jupyter lab $notebookPath.Path
} else {
    throw "Jupyter was not found on PATH. Install Jupyter before launching the Chapter 13 notebook."
}