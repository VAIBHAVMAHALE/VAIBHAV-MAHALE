# Activate venv (PowerShell)
if (-not (Test-Path .\venv\Scripts\Activate.ps1)) {
  Write-Error "Virtual environment not found. Create it with: python -m venv venv"
  exit 1
}

.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt

# Run pytest (will start backend/frontend in test fixture)
pytest -q
