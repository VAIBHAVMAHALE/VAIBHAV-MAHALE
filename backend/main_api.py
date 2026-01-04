from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Simple in-memory store for smoke tests (replace with real DB later)
_users = {}

class RegisterIn(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class LoginIn(BaseModel):
    username: str
    password: str

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.post('/auth/register')
def register(payload: RegisterIn):
    if payload.email in _users:
        raise HTTPException(400, detail='user exists')
    _users[payload.email] = { 'email': payload.email, 'password': payload.password, 'name': payload.name }
    return { 'status': 'ok' }

@app.post('/auth/login')
def login(payload: LoginIn):
    u = _users.get(payload.username)
    if not u or u.get('password') != payload.password:
        raise HTTPException(401, detail='invalid credentials')
    token = f'fake-token-{payload.username}'
    return { 'access_token': token, 'token_type': 'bearer' }

@app.get('/auth/me')
def me(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(401, detail='missing token')
    token = authorization.split(' ',1)[1]
    if not token.startswith('fake-token-'):
        raise HTTPException(401, detail='invalid token')
    email = token[len('fake-token-'):]
    u = _users.get(email)
    if not u:
        raise HTTPException(401, detail='invalid token')
    return { 'email': u['email'], 'name': u.get('name') }

