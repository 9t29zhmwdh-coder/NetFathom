# Local development, Windows PowerShell
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    .\.venv\Scripts\pip install --upgrade pip
    .\.venv\Scripts\pip install -e ".[dev]"
}

Write-Host "NetFathom venv ready."
Write-Host "Activate: .\.venv\Scripts\Activate.ps1"
Write-Host "Run:      netfathom --help"
Write-Host ""
Write-Host "Note: ARP sweep and SYN scan require Administrator."
Write-Host "Run PowerShell as Administrator for full functionality."
