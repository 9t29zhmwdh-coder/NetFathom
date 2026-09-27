# Local development, Windows PowerShell
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    # Same hashed lock as CI, so a fresh venv gets exactly the tested versions.
    .\.venv\Scripts\python -m pip install --require-hashes -r requirements/ci.txt
    .\.venv\Scripts\python -m pip install --no-deps --no-build-isolation -e .
}

Write-Host "NetFathom venv ready."
Write-Host "Activate: .\.venv\Scripts\Activate.ps1"
Write-Host "Run:      netfathom --help"
Write-Host ""
Write-Host "Note: ARP sweep and SYN scan require Administrator."
Write-Host "Run PowerShell as Administrator for full functionality."
