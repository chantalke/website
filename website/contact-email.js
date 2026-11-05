// Let visitors copy the address without launching a default mail application.
(() => {
  const en = document.documentElement.lang === 'en';
  const email = 'chantalke@gmail.com';
  const dialog = document.createElement('dialog');
  dialog.className = 'email-dialog';
  dialog.setAttribute('aria-labelledby', 'email-title');
  dialog.innerHTML = `<button type="button" class="close" aria-label="${en ? 'Close' : 'Sluiten'}">×</button><h2 id="email-title">${en ? 'Send me an email' : 'Mail me gerust'}</h2><p>${en ? 'Copy my address and use your own email app.' : 'Kopieer mijn adres en gebruik je eigen mailprogramma.'}</p><input readonly aria-label="${en ? 'Email address' : 'E-mailadres'}" value="${email}"><button type="button" class="email-copy">${en ? 'Copy email address' : 'Kopieer e-mailadres'}</button><p class="email-status" role="status" aria-live="polite"></p>`;
  document.body.append(dialog);
  const input = dialog.querySelector('input');
  dialog.querySelector('.close').addEventListener('click', () => dialog.close());
  dialog.querySelector('.email-copy').addEventListener('click', async () => {
    const status = dialog.querySelector('.email-status');
    try {
      await navigator.clipboard.writeText(email);
      status.textContent = en ? 'Copied! Paste it into your email app.' : 'Gekopieerd! Plak het in je mailprogramma.';
    } catch {
      input.focus(); input.select();
      status.textContent = en ? 'Select and copy the address above.' : 'Selecteer en kopieer het adres hierboven.';
    }
  });
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="mailto:"]');
    if (!link) return;
    event.preventDefault();
    dialog.querySelector('.email-status').textContent = '';
    dialog.showModal();
  });
})();
