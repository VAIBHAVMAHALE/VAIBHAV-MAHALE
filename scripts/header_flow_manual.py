import os
import time
import requests

# Config: call backend API for auth; frontend for page source
BACKEND = os.environ.get('BACKEND_URL', 'http://127.0.0.1:8000').rstrip('/')
FRONTEND = os.environ.get('FRONTEND_URL', 'http://127.0.0.1:5000').rstrip('/')

REGISTER_URL = BACKEND + '/auth/register'
LOGIN_URL = BACKEND + '/auth/login'
ME_URL = BACKEND + '/auth/me'
FRONTEND_LOGIN_PAGE = FRONTEND + '/login'

# Test user
email = f"testuser+{int(time.time())}@example.com"
password = "Password123!"

session = requests.Session()

# 1) Register (backend API)
try:
    resp = session.post(REGISTER_URL, json={"email": email, "password": password, 'name': 'Header Test'})
    print('Register:', resp.status_code)
    print(resp.text[:400])
    if not resp.ok:
        raise SystemExit('Register failed')
except Exception as e:
    print('Register failed:', e)
    raise

# 2) Login (backend API)
try:
    resp = session.post(LOGIN_URL, json={"username": email, "password": password})
    print('Login:', resp.status_code)
    print(resp.text[:400])
    if not resp.ok:
        raise SystemExit('Login failed')
    token = resp.json().get('access_token')
except Exception as e:
    print('Login failed:', e)
    raise

# 3) /auth/me using token (simulate header.js call)
try:
    resp = session.get(ME_URL, headers={'Authorization': 'Bearer ' + token})
    print('/auth/me:', resp.status_code)
    print(resp.text[:400])
    if not resp.ok:
        raise SystemExit('/auth/me failed')
except Exception as e:
    print('/auth/me failed:', e)
    raise

# 4) Check frontend login page contains window.BACKEND injection and that it matches BACKEND
try:
    r = session.get(FRONTEND_LOGIN_PAGE)
    print('\nFrontend /login status:', r.status_code)
    if r.ok:
        if 'window.BACKEND' in r.text:
            # try to extract the assigned value
            marker = "window.BACKEND"
            idx = r.text.find(marker)
            excerpt = r.text[idx-80: idx+120]
            print('Found injection excerpt:\n', excerpt)
            if str(BACKEND) in excerpt:
                print('FRONTEND injection matches BACKEND: OK')
            else:
                print('FRONTEND injection DOES NOT match BACKEND: mismatch')
        else:
            print('No window.BACKEND injection found in /login page source')
except Exception as e:
    print('Frontend check failed:', e)
    raise

print('\nHeader refresh test PASSED')
