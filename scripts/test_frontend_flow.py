import requests

BASE='http://127.0.0.1:8000'

def register(email='test+auto@example.com'):
    r=requests.post(BASE+'/auth/register',json={'email':email,'password':'secret123','name':'Auto Test'})
    print('register', r.status_code, r.text)
    return r

def login(email='test+auto@example.com'):
    r=requests.post(BASE+'/auth/login',json={'username':email,'password':'secret123'})
    print('login', r.status_code, r.text)
    if r.ok:
        return r.json().get('access_token')
    return None


def me(token):
    r=requests.get(BASE+'/auth/me', headers={'Authorization': 'Bearer '+token})
    print('me', r.status_code, r.text)
    return r

if __name__=='__main__':
    register('test+auto@example.com')
    token=login('test+auto@example.com')
    if token:
        me(token)
    else:
        print('login failed')
