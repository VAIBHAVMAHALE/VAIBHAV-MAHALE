document.addEventListener('DOMContentLoaded', () => {
  const BACKEND = (window.BACKEND || 'http://127.0.0.1:8000').replace(/\/$/, '');
  const loginBtn = document.getElementById('login');
  const toReg = document.getElementById('to-register');
  const email = document.getElementById('email');
  const pass = document.getElementById('password');
  const msg = document.getElementById('login-msg');

  loginBtn.addEventListener('click', async () => {
    msg.textContent = 'Logging in...';
    try {
      const resp = await fetch(BACKEND + '/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username: email.value, password: pass.value }) });
      const j = await resp.json();
      if (resp.ok) {
        localStorage.setItem('access_token', j.access_token);
        msg.textContent = 'Logged in. Redirecting...';
        setTimeout(() => window.location.href = '/tasks', 700);
      } else {
        msg.textContent = j.detail || JSON.stringify(j);
      }
    } catch (err) {
      msg.textContent = 'Request failed: ' + err;
    }
  });

  toReg.addEventListener('click', () => { window.location.href = '/register'; });
});