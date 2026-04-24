$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $projectRoot

if (Get-Command py -ErrorAction SilentlyContinue) {
    py -m http.server 8508
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    python -m http.server 8508
} else {
    throw "Python was not found on PATH. Install Python before serving the frontend."
}