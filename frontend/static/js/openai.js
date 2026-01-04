document.addEventListener('DOMContentLoaded', () => {
  const BACKEND = (window.BACKEND || 'http://127.0.0.1:8000').replace(/\/$/, '');
  const send = document.getElementById('send');
  const prompt = document.getElementById('prompt');
  const result = document.getElementById('result');
  const status = document.getElementById('status');

  send.addEventListener('click', async () => {
    status.textContent = 'Sending...';
    try {
      const resp = await fetch(BACKEND + '/generate_openai', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ prompt: prompt.value }) });
      const j = await resp.json();
      if (resp.ok) {
        result.textContent = j.text || JSON.stringify(j);
        document.getElementById('meta-model').textContent = j.meta.model || '—';
        document.getElementById('meta-latency').textContent = j.meta.latency_ms || '—';
        document.getElementById('meta-total').textContent = j.meta.total_tokens || '—';
        document.getElementById('meta-prompt').textContent = j.meta.prompt_tokens || '—';
        document.getElementById('meta-completion').textContent = j.meta.completion_tokens || '—';
        status.textContent = 'Done';
      } else {
        status.textContent = 'Request failed';
      }
    } catch (e) {
      status.textContent = 'Error: ' + e;
    }
  });
});