document.addEventListener('DOMContentLoaded', () => {
  const BACKEND = (window.BACKEND || 'http://127.0.0.1:8000').replace(/\/$/, '');
  const token = () => localStorage.getItem('access_token');

  const createBtn = document.getElementById('create');
  const titleEl = document.getElementById('title');
  const descEl = document.getElementById('desc');
  const tasksList = document.getElementById('tasks');

  async function list() {
    tasksList.innerHTML = 'Loading...';
    try {
      const resp = await fetch(BACKEND + '/tasks', { headers: { 'Authorization': 'Bearer ' + token() } });
      if (!resp.ok) throw new Error('unauth');
      const arr = await resp.json();
      tasksList.innerHTML = '';
      for (const t of arr) {
        const li = document.createElement('li');
        li.textContent = `${t.title} — ${t.status}`;
        li.addEventListener('click', () => { alert(JSON.stringify(t)); });
        tasksList.appendChild(li);
      }
    } catch (e) {
      tasksList.innerHTML = 'Failed to load tasks. Are you logged in?';
    }
  }

  createBtn.addEventListener('click', async () => {
    try {
      const resp = await fetch(BACKEND + '/tasks', { method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token() }, body: JSON.stringify({ title: titleEl.value, description: descEl.value }) });
      if (!resp.ok) throw new Error('create failed');
      titleEl.value = '';
      descEl.value = '';
      list();
    } catch (e) {
      alert('Create failed: ' + e);
    }
  });

  list();
});