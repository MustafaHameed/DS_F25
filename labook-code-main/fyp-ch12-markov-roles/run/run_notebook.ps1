$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$notebookPath = Resolve-Path (Join-Path $projectRoot "..\ch12-markov\ch12-markov.ipynb")

Set-Location (Split-Path $notebookPath.Path)

if (Get-Command jupyter -ErrorAction SilentlyContinue) {
    jupyter lab $notebookPath.Path
} else {
    throw "Jupyter was not found on PATH. Install Jupyter before launching the Chapter 12 notebook."
}