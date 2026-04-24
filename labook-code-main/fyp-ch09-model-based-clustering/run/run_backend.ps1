$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$backendScript = Join-Path $projectRoot "backend\run_model_based_pipeline.py"

Set-Location $projectRoot

if (Get-Command py -ErrorAction SilentlyContinue) {
    py $backendScript
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    python $backendScript
} else {
    throw "Python was not found on PATH. Install Python before running the backend."
}