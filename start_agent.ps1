$ErrorActionPreference = "Stop"

if (Test-Path ".env") {
  Get-Content ".env" | ForEach-Object {
    if ($_ -match "^\s*#" -or $_ -notmatch "=") { return }
    $key, $value = $_ -split "=", 2
    [Environment]::SetEnvironmentVariable($key.Trim(), $value.Trim(), "Process")
  }
}

python -m pip install -r requirements.txt
python run_orchestrator.py

