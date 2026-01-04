document.addEventListener('DOMContentLoaded', async () => {
  const BACKEND = (window.BACKEND || 'http://127.0.0.1:8000').replace(/\/$/, '');
  const loginLink = document.getElementById('header-login');
  const regLink = document.getElementById('header-register');
  const logoutBtn = document.getElementById('header-logout');
  const userSpan = document.getElementById('header-user');

  function token() { return localStorage.getItem('access_token'); }

  async function refresh() {
    const t = token();
    if (!t) {
      userSpan.textContent = 'Not logged in';
      loginLink.style.display = '';
      regLink.style.display = '';
      logoutBtn.style.display = 'none';
      return;
    }
    try {
      const resp = await fetch(BACKEND + '/auth/me', { headers: { 'Authorization': 'Bearer ' + t } });
      if (!resp.ok) throw new Error('not authenticated');
      const user = await resp.json();
      userSpan.textContent = user.email || user.name || user.id;
      loginLink.style.display = 'none';
      regLink.style.display = 'none';
      logoutBtn.style.display = '';
    } catch (e) {
      localStorage.removeItem('access_token');
      userSpan.textContent = 'Not logged in';
      loginLink.style.display = '';
      regLink.style.display = '';
      logoutBtn.style.display = 'none';
    }
  }

  logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('access_token');
    refresh();
    window.location.href = '/login';
  });

  refresh();
});