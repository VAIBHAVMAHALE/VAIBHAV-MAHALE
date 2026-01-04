import os
import subprocess
import sys
import time
import signal
import requests

BACKEND = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000").rstrip('/')
FRONTEND = os.environ.get("FRONTEND_URL", "http://127.0.0.1:5000").rstrip('/')

PY = sys.executable


def wait_for(url, timeout=10.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=1.0)
            return r
        except Exception:
            time.sleep(0.2)
    raise RuntimeError(f"{url} not available after {timeout}s")


def start_process(cmd, cwd=None):
    return subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def terminate_process(p):
    try:
        if p.poll() is None:
            p.send_signal(signal.SIGINT)
            time.sleep(0.5)
            if p.poll() is None:
                p.terminate()
    except Exception:
        pass


def test_header_flow_e2e():
    # Start backend and frontend using same interpreter
    backend_cmd = [PY, "-m", "uvicorn", "backend.main_api:app", "--host", "127.0.0.1", "--port", "8000"]
    frontend_cmd = [PY, "frontend/app.py"]

    p_backend = start_process(backend_cmd, cwd=os.getcwd())
    try:
        wait_for(BACKEND + "/")

        p_frontend = start_process(frontend_cmd, cwd=os.getcwd())
        try:
            wait_for(FRONTEND + "/")

            # Register
            email = f"pytest-header-{int(time.time())}@example.com"
            pwd = "secret123"
            r = requests.post(BACKEND + "/auth/register", json={"email": email, "password": pwd, "name": "PyTest"})
            assert r.ok, f"register failed: {r.status_code} {r.text}"

            # Login
            r = requests.post(BACKEND + "/auth/login", json={"username": email, "password": pwd})
            assert r.ok, f"login failed: {r.status_code} {r.text}"
            token = r.json().get("access_token")
            assert token

            # Check /auth/me
            r = requests.get(BACKEND + "/auth/me", headers={"Authorization": "Bearer " + token})
            assert r.ok and r.json().get("email") == email

            # Check frontend injection
            r = requests.get(FRONTEND + "/login")
            assert r.ok
            assert "window.BACKEND" in r.text
            assert BACKEND in r.text

        finally:
            terminate_process(p_frontend)
    finally:
        terminate_process(p_backend)
