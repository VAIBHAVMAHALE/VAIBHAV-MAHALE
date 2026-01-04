AI Personal Assistant (local dev)

Frontend configuration

- Set BACKEND_URL environment variable to point the frontend to a different backend host/port.
  Example (PowerShell):
    $env:BACKEND_URL='http://127.0.0.1:8000'

- The Flask frontend injects `window.BACKEND` into pages using the value of `BACKEND_URL` (fallback: `http://127.0.0.1:8000`).

- Restart the frontend server after changing the env var so the templates pick up the new value.

Developer testing and CI

- Dev requirements are in `requirements-dev.txt` and include `pytest` and `requests`.

- Run tests locally (in your venv):
  - PowerShell: `.\venv\Scripts\Activate.ps1` then `python -m pip install -r requirements-dev.txt` then `pytest -q` or run `scripts\run_tests.ps1`.
  - POSIX: `pip install -r requirements-dev.txt && pytest -q` or run `scripts/run_tests.sh`.

- A GitHub Actions workflow is provided at `.github/workflows/ci.yml` that starts backend and frontend, then runs the tests.
